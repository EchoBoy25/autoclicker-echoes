

-- 🌱 Grow a Garden Auto-Buyer with OCR, Live Stats, and Logging
-- ⌨️ Option+G to start, Option+S to pause

local botEnabled = false
local seedTimer = nil
local paused = false
local delayBetweenSeeds = 0.4
local delayBetweenClicks = 0.12
local clickAttempts = 10
local loopInterval = 300

-- Seed names to track
local seedNames = {
    "Tomato", "Cauliflower", "Watermelon",
    "Green Apple", "Avocado", "Banana",
    "Pineapple", "Kiwi", "Bell Pepper", "Prickly Pear",
    "Loquat", "Feijoa", "Sugar Apple"
}

-- Seed stats
local seedStats = {}
for _, name in ipairs(seedNames) do seedStats[name] = 0 end

-- Log file path
local logPath = "/home/sandbox/Desktop/seed_log.txt"

-- Click and scan coordinates
local seedRegions = {
    {click = {x=920, y=750}, scan = {x=880, y=735, w=120, h=30}, label="Seed 1"},
    {click = {x=920, y=680}, scan = {x=880, y=665, w=120, h=30}, label="Seed 2"},
    {click = {x=920, y=610}, scan = {x=880, y=595, w=120, h=30}, label="Seed 3"},
    {click = {x=920, y=540}, scan = {x=880, y=525, w=120, h=30}, label="Seed 4"},
    {click = {x=920, y=470}, scan = {x=880, y=455, w=120, h=30}, label="Seed 5"},
    {click = {x=920, y=400}, scan = {x=880, y=385, w=120, h=30}, label="Seed 6"},
}

function jitterMouse(x, y)
    local jx = x + math.random(-3, 3)
    local jy = y + math.random(-3, 3)
    hs.mouse.setAbsolutePosition({x=jx, y=jy})
end

function extractText(scan)
    local img = hs.screen.mainScreen():snapshot(scan)
    local path = "/tmp/ocr_temp_" .. tostring(math.random(10000)) .. ".png"
    img:saveToFile(path)
    local output = hs.execute("tesseract '" .. path .. "' stdout", true)
    return output
end

function regionHasStock(scan)
    local text = extractText(scan)
    return not string.find(text:lower(), "no stock")
end

function matchSeedName(text)
    for _, name in ipairs(seedNames) do
        if string.find(text:lower(), name:lower()) then return name end
    end
    return nil
end

function logSeed(seedName, count)
    local timestamp = os.date("%Y-%m-%d %H:%M:%S")
    local entry = string.format("[%s] Bought %dx %s\n", timestamp, count, seedName)
    local file = io.open(logPath, "a")
    if file then
        file:write(entry)
        file:close()
    end
end

function clickSeedIfStock(seed)
    local rawText = extractText(seed.scan)
    if regionHasStock(seed.scan) then
        local matchedName = matchSeedName(rawText)
        if matchedName then
            local purchased = 0
            for i = 1, clickAttempts do
                jitterMouse(seed.click.x, seed.click.y)
                hs.eventtap.leftClick(seed.click)
                hs.timer.usleep(delayBetweenClicks * 1e6)
                seedStats[matchedName] = seedStats[matchedName] + 1
                purchased = purchased + 1
                updateStatsDisplay()
            end
            logSeed(matchedName, purchased)
        end
    end
end

function buyAllRareSeeds()
    if paused then return end
    for _, seed in ipairs(seedRegions) do
        clickSeedIfStock(seed)
        hs.timer.usleep(delayBetweenSeeds * 1e6)
    end
end

function toggleBot()
    botEnabled = not botEnabled
    if botEnabled then
        hs.alert.show("🌿 Seed Bot ON")
        seedTimer = hs.timer.doEvery(loopInterval, buyAllRareSeeds)
        buyAllRareSeeds()
        miniConsole:show()
        statsView:show()
    else
        hs.alert.show("🌿 Seed Bot OFF")
        if seedTimer then seedTimer:stop() end
        miniConsole:hide()
        statsView:hide()
    end
end

function pauseBot()
    paused = true
    hs.alert.show("⏸ Bot Paused")
end

-- Hotkeys
hs.hotkey.bind({"alt"}, "g", toggleBot)
hs.hotkey.bind({"alt"}, "s", pauseBot)

-- Mini toggle UI
miniConsole = hs.webview.new({x=40, y=40, w=160, h=80})
    :windowStyle("utility")
    :allowGestures(false)
    :allowNewWindows(false)
    :title("Auto Buyer")
    :html([[
        <html><body style="margin:0;padding:0;font-family:sans-serif;font-size:14px;
        background:#111;color:#0ff;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;">
        <div>🌱 Seed Bot</div>
        <button onclick="hammerspoon.call('stop')" style="margin-top:10px;">Pause</button>
        </body></html>
    ]])
    :allowTextEntry(false)

-- Live stats view
function formatStats()
    local html = "<div style='font-family:sans-serif;font-size:13px;background:#111;color:#0ff;padding:10px;'>"
    html = html .. "<h3>🌿 Seed Counter</h3><ul style='padding-left: 1em;'>"
    for _, name in ipairs(seedNames) do
        html = html .. string.format("<li>%s: %d</li>", name, seedStats[name])
    end
    html = html .. "</ul></div>"
    return html
end

function updateStatsDisplay()
    statsView:html(formatStats())
end

statsView = hs.webview.new({x=220, y=40, w=220, h=400})
    :windowStyle("utility")
    :allowGestures(false)
    :allowNewWindows(false)
    :title("Seed Tracker")
    :html(formatStats())
    :allowTextEntry(false)
    :hide()

-- Pause button callback
hs.webview.usercontent.setCallback(miniConsole, "stop", function()
    pauseBot()
end)

hs.alert.show("🌿 Seed Buyer Ready (Option+G to start, Option+S to pause)")