--[[
OpenBlox backpack HUD script, written by DangerOnTheRanger

Copyright 2011 DangerOnTheRanger

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
--]]


function is_tool(element)
	if element['equip'] != nil and element['unequip'] != nil then
		return true
	else
		return false
end


function reparent_to_player(player)
	Script.parent = player
end

World.on_player_joined.add_handler(reparent_to_player)


current_backpack_tools = {}
equipped_tool = nil
gui_factory = LuaFactory.make('WidgetFactory')
backpack_position = LuaFactory.make('Vector2D', 0, -50)
backpack_container = gui_factory.make('container',
									  gui_factory.HORIZONTAL_LAYOUT_MANAGER,
									  backpack_position)

function tool_watcher(task)
	
	for element in python.iterex(Script.parent.children.itervalues()) do
		
		if is_tool(element) == true then
			if tool_in_backpack(element) then
				add_tool_to_backpack(element)
			end
		end
	end
	
	for tool in current_backpack_tools do
		if Script.parent.children[tool.name] == nil then
			remove_tool_from_backpack(tool)
		end
	end
	
	return task.AGAIN
end


function tool_in_backpack(tool)
	if current_backpack_tools[tool.name] != nil then
		return true
	else
		return false
end


function add_tool_to_backpack(tool)
end