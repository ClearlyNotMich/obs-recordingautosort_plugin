/*
OBS Recording Autosort scaffold
Based on the OBS plugin template; see the repository's attribution notes.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see <https://www.gnu.org/licenses/>
*/

#include <obs-module.h>

#include <plugin-macros.generated.h>

OBS_DECLARE_MODULE()
OBS_MODULE_USE_DEFAULT_LOCALE(PLUGIN_NAME, "en-US")

const char *obs_module_name(void)
{
	return PLUGIN_NAME " (scaffold)";
}

const char *obs_module_description(void)
{
	return PLUGIN_DESCRIPTION;
}

bool obs_module_load(void)
{
	blog(LOG_INFO,
	     "scaffold loaded (version %s); recording sorting is not implemented",
	     PLUGIN_VERSION);
	return true;
}

void obs_module_unload(void)
{
	blog(LOG_INFO, "plugin unloaded");
}
