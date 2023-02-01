
type pixel_data = { [number] : number }
type pixel_column = { [number] : pixel_data }
type pixel_array = { [number] : pixel_column }

local Module = { }

local baseFrame : Frame = Instance.new('Frame')
baseFrame.Name = "TemplatePixel"
baseFrame.BackgroundColor3 = Color3.new()
baseFrame.BorderSizePixel = 0
baseFrame.Size = UDim2.fromOffset(1, 1)
function Module:PixelToFrame( pixel_data : pixel_data )
	local r : number, g : number, b : number, alpha : number = unpack( pixel_data )
	local Frame = baseFrame:Clone()
	Frame.Name = string.format("r:%s g:%s b:%s a: %s", r, g, b, alpha)
	Frame.BackgroundColor3 = Color3.fromRGB(r, g, b)
	Frame.BackgroundTransparency = (alpha / 255)
	return Frame
end

function Module:RenderPixelsAsFrames( pixel_array : pixel_array ) : { Frame }
	local Frames : { Frame } = { }
	for x : number, t : pixel_column in ipairs(  pixel_array ) do
		for y : number, pixel_data : pixel_data in ipairs( t ) do
			table.insert( Frames, Module:PixelToFrame( pixel_data ) )
		end
		task.wait()
	end
	return Frames
end

return Module
