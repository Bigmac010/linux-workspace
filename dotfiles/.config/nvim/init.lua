-- Optional editor; install with "bash install.sh --dotfiles".
vim.g.mapleader = " "
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.expandtab = true
vim.opt.shiftwidth = 4
vim.opt.tabstop = 4
vim.opt.ignorecase = true
vim.opt.smartcase = true
-- VimTeX provides editing/navigation; the shared builder owns compilation.
vim.g.vimtex_compiler_enabled = 0
vim.g.vimtex_view_enabled = 0
local timers = {}
local function compile()
    local main = vim.b.vimtex and vim.b.vimtex.tex or vim.api.nvim_buf_get_name(0)
    vim.fn.jobstart({"lw", "build", main}, {
        on_exit = function(_, code)
            if code ~= 0 then
                vim.schedule(function() vim.notify("LaTeX build failed; run :LatexBuild for output", vim.log.levels.ERROR) end)
            end
        end,
    })
end
vim.api.nvim_create_user_command("LatexBuild", function()
    local main = vim.b.vimtex and vim.b.vimtex.tex or vim.api.nvim_buf_get_name(0)
    vim.cmd("!" .. vim.fn.shellescape("lw") .. " build " .. vim.fn.shellescape(main))
end, {})
local group = vim.api.nvim_create_augroup("workspace_latex", {clear=true})
vim.api.nvim_create_autocmd({"TextChanged", "TextChangedI"}, {
    pattern="*.tex", group=group, callback=function(event)
        local buf=event.buf
        if timers[buf] then vim.fn.timer_stop(timers[buf]) end
        timers[buf]=vim.fn.timer_start(500,function()
            timers[buf]=nil
            if vim.api.nvim_buf_is_valid(buf) and vim.bo[buf].modified and not vim.bo[buf].readonly then
                vim.api.nvim_buf_call(buf,function() vim.cmd("update") end)
            end
        end)
    end,
})
vim.api.nvim_create_autocmd("BufWritePost", {pattern="*.tex",group=group,callback=compile})
vim.api.nvim_create_autocmd("BufWipeout", {group=group,callback=function(event)
    if timers[event.buf] then vim.fn.timer_stop(timers[event.buf]); timers[event.buf]=nil end
end})
-- Do not delete caches or SyncTeX on exit.
