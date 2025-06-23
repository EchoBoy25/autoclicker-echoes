
local clicking = false
local keySpamming = false
local clickTimer = nil
local keyTimer = nil
local clickCount = 0
local clickInterval = 0.1
local keyInterval = 0.2
local keyToSpam = "space"

local menu = hs.menubar.new()
menu:setTitle("🎮")

function startClicking()
    if clicking then return end
    clicking = true
    clickTimer = hs.timer.doWhile(
        function() return clicking end,
        function()
            hs.eventtap.leftClick(hs.mouse.getAbsolutePosition())
            clickCount = clickCount + 1
        end,
        clickInterval + math.random(-10, 10)/1000
    )
end

function stopClicking()
    clicking = false
    if clickTimer then
        clickTimer:stop()
        clickTimer = nil
    end
end

function toggleClicking()
    if clicking then stopClicking() else startClicking() end
    refreshMenu()
end

function startKeySpammer()
    if keySpamming then return end
    keySpamming = true
    keyTimer = hs.timer.doWhile(
        function() return keySpamming end,
        function()
            hs.eventtap.keyStroke({}, keyToSpam)
        end,
        keyInterval + math.random(-10, 10)/1000
    )
end

function stopKeySpammer()
    keySpamming = false
    if keyTimer then
        keyTimer:stop()
        keyTimer = nil
    end
end

function toggleKeySpammer()
    if keySpamming then stopKeySpammer() else startKeySpammer() end
    refreshMenu()
end

function panicStop()
    stopClicking()
    stopKeySpammer()
    hs.alert("⛔ Panic Stop Activated")
end

function refreshMenu()
    menu:setMenu({
        { title = clicking and "✅ Stop Clicking" or "▶️ Start Clicking", fn = toggleClicking },
        { title = keySpamming and "✅ Stop Key Spam" or "▶️ Start Key Spam", fn = toggleKeySpammer },
        { title = "🔢 Clicks: " .. clickCount, disabled = true },
        { title = "⛔ Panic Stop", fn = panicStop },
        { title = "❌ Quit", fn = function() hs.application.frontmostApplication():kill() end }
    })
end

hs.hotkey.bind({"alt"}, "c", toggleClicking)
hs.hotkey.bind({"alt"}, "k", toggleKeySpammer)
hs.hotkey.bind({"alt", "shift"}, "p", panicStop)

refreshMenu()
