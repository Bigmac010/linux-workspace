vim.g.mapleader = " "

vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.mouse = "a"
vim.opt.expandtab = true
vim.opt.shiftwidth = 4
vim.opt.tabstop = 4
vim.opt.smartindent = true
vim.opt.wrap = false
vim.opt.ignorecase = true
vim.opt.smartcase = true

local lazy_path = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
local uv = vim.uv or vim.loop

if not uv.fs_stat(lazy_path) then
    local result = vim.fn.system({
        "git",
        "clone",
        "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git",
        "--branch=stable",
        lazy_path,
    })

    if vim.v.shell_error ~= 0 then
        error("Failed to install lazy.nvim:\n" .. result)
    end
end

vim.opt.rtp:prepend(lazy_path)

require("lazy").setup({
    {
        "lervag/vimtex",
        lazy = false,
        init = function()
            vim.g.vimtex_compiler_method = "latexmk"
            vim.g.vimtex_quickfix_mode = 0

            if vim.env.CODESPACES == "true" then
                vim.g.vimtex_view_enabled = 0
            else
                vim.g.vimtex_view_method = "zathura"
            end
        end,
    },
})

local vimtex_group = vim.api.nvim_create_augroup(
    "vimtex_live_compile",
    { clear = true }
)

vim.api.nvim_create_autocmd("User", {
    pattern = "VimtexEventInitPost",
    group = vimtex_group,
    command = "VimtexCompile!",
})

local tex_save_timer = nil

vim.api.nvim_create_autocmd(
    { "TextChanged", "TextChangedI", "TextChangedP" },
    {
        pattern = "*.tex",
        group = vimtex_group,
        callback = function(args)
            if tex_save_timer then
                vim.fn.timer_stop(tex_save_timer)
            end

            local buffer = args.buf

            tex_save_timer = vim.fn.timer_start(200, function()
                tex_save_timer = nil

                if vim.api.nvim_buf_is_valid(buffer)
                    and vim.api.nvim_buf_is_loaded(buffer)
                    and vim.bo[buffer].modified then
                    vim.api.nvim_buf_call(buffer, function()
                        vim.cmd("silent! update")
                    end)
                end
            end)
        end,
    }
)

