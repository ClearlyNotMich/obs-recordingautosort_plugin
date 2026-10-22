#!/usr/bin/env python3
"""Offline Linux CMake/compile fixture, NOT an OBS integration or ABI test.

Requires Python 3, CMake and local C/C++ build tools. It copies the build inputs
to a temporary directory, supplies a deliberately minimal fake libobs target,
and checks scaffold metadata and logging through a fake host. It never installs
dependencies, launches OBS, touches recordings, or creates release packages.
"""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


FAKE_OBS_HEADER = r"""
#ifndef SCAFFOLD_TEST_FAKE_OBS_MODULE_H
#define SCAFFOLD_TEST_FAKE_OBS_MODULE_H
#include <stdbool.h>
#define OBS_DECLARE_MODULE()
#define OBS_MODULE_USE_DEFAULT_LOCALE(name, locale)
enum { LOG_INFO = 200 };
void blog(int level, const char *format, ...);
const char *obs_module_name(void);
const char *obs_module_description(void);
bool obs_module_load(void);
void obs_module_unload(void);
#endif
"""

FAKE_HOST = r"""
#include <obs-module.h>
#include <assert.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>

static int log_count;
static char last_message[512];

void blog(int level, const char *format, ...)
{
    va_list arguments;
    assert(level == LOG_INFO);
    va_start(arguments, format);
    vsnprintf(last_message, sizeof(last_message), format, arguments);
    va_end(arguments);
    ++log_count;
}

int main(void)
{
    assert(strcmp(obs_module_name(), @NAME@ " (scaffold)") == 0);
    assert(strstr(obs_module_description(), "sorting is not implemented"));
    assert(obs_module_load());
    assert(log_count == 1);
    assert(strstr(last_message, "[" @NAME@ "]"));
    assert(strstr(last_message, "sorting is not implemented"));
    assert(strstr(last_message, @VERSION@));
    obs_module_unload();
    assert(log_count == 2);
    assert(strstr(last_message, "plugin unloaded"));
    puts("Fake-host metadata and load/unload logging checks passed.");
    return 0;
}
"""


def run(command):
    subprocess.run([str(part) for part in command], check=True, timeout=120)


def cache_value(cache, key, kind):
    prefix = key + ":" + kind + "="
    for line in cache.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):]
    raise AssertionError("Missing CMake cache entry: " + key)


def check(root, temporary):
    source = temporary / "source"
    source.mkdir()
    for name in ("CMakeLists.txt", "buildspec.json"):
        shutil.copy2(root / name, source / name)
    for name in ("src", "cmake", "data"):
        if (root / name).is_dir():
            ignored = shutil.ignore_patterns("*.generated.*") if name == "src" else None
            shutil.copytree(root / name, source / name, ignore=ignored)
    specification = json.loads((source / "buildspec.json").read_text())
    name, version = specification["name"], specification["version"]

    fake = temporary / "fake-libobs"
    include = fake / "include"
    package = fake / "lib/cmake/libobs"
    include.mkdir(parents=True)
    package.mkdir(parents=True)
    (include / "obs-module.h").write_text(FAKE_OBS_HEADER)
    (package / "libobsConfig.cmake").write_text(
        "# Deliberate test double: this does not provide OBS itself.\n"
        "add_library(OBS::libobs INTERFACE IMPORTED)\n"
        "set_target_properties(OBS::libobs PROPERTIES "
        'INTERFACE_INCLUDE_DIRECTORIES "${CMAKE_CURRENT_LIST_DIR}/../../../include")\n'
    )

    build = temporary / "build"
    configure = ["cmake", "-S", source, "-B", build, "-DCMAKE_BUILD_TYPE=Debug",
                 "-Dlibobs_DIR=" + str(package), "-DCCACHE_SUPPORT=OFF"]
    run(configure)
    generated = build / "generated/plugin-macros.generated.h"
    assert generated.is_file(), "Generated header must be in the build directory"
    source_header = source / "src/plugin-macros.generated.h"
    assert not source_header.exists(), "Configure must not create a source-tree header"
    header = generated.read_text()
    assert '#define PLUGIN_NAME "' + name + '"' in header
    assert '#define PLUGIN_VERSION "' + version + '"' in header
    cache = (build / "CMakeCache.txt").read_text()
    assert cache_value(cache, "PLUGIN_AUTHOR", "STRING") == ""
    assert cache_value(cache, "LINUX_MAINTAINER_EMAIL", "STRING") == ""

    # A header left by the old build must not shadow the current binary header.
    stale = "#error Stale source-tree generated header must never be included\n"
    source_header.write_text(stale)
    run(configure + ["-DPLUGIN_AUTHOR=Fixture Publisher",
                     "-DLINUX_MAINTAINER_EMAIL=fixture@example.invalid",
                     "-DMACOS_BUNDLEID=invalid.example.scaffold-fixture"])
    assert source_header.read_text() == stale, "Configure overwrote an existing source header"
    cache = (build / "CMakeCache.txt").read_text()
    assert cache_value(cache, "PLUGIN_AUTHOR", "STRING") == "Fixture Publisher"
    assert cache_value(cache, "LINUX_MAINTAINER_EMAIL", "STRING") == "fixture@example.invalid"
    assert cache_value(cache, "MACOS_BUNDLEID", "STRING") == "invalid.example.scaffold-fixture"
    run(["cmake", "--build", build, "--target", name, "--parallel", "2"])
    assert (build / (name + ".so")).is_file(), "Named module was not built"

    host = temporary / "fake-host.c"
    host.write_text(FAKE_HOST.replace("@NAME@", json.dumps(name)).replace("@VERSION@", json.dumps(version)))
    executable = temporary / "fake-host"
    compiler = cache_value(cache, "CMAKE_C_COMPILER", "FILEPATH")
    run([compiler, "-std=gnu11", "-Wall", "-Wextra", "-Werror", "-Wstrict-prototypes",
         "-I" + str(include), "-I" + str(generated.parent), "-I" + str(source / "src"),
         source / "src/plugin-main.c", host, "-o", executable])
    run([executable])
    assert source_header.read_text() == stale
    print("PASS: offline Linux scaffold fixture; real libobs/OBS ABI and platform packaging remain untested.")


def main():
    if not sys.platform.startswith("linux"):
        raise SystemExit("This offline fixture currently supports Linux build tools only.")
    if shutil.which("cmake") is None:
        raise SystemExit("CMake is required; this check does not install it.")
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="obs-scaffold-check-") as directory:
        check(root, Path(directory))


if __name__ == "__main__":
    main()
