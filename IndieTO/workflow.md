背景：开发并且上线了一个工具导航站 indieto.com，基于 mkdirs 导航站模版，但一个个上传速度太慢了。于是我想打造一个工作流，目前工作流构思如下：

最终实现的效果：
打开某个想要收集的网站，点击某个按钮(浏览器插件或者书签)，打开我制作的工作流网站，开始执行，经过自动联网收集和 AI 处理以及人工校验之后，在电脑本地的 IndieTO/toolname/ 目录下得到四个文件，分别是是介绍文章，logo，screenshot，以及上传到后台的 json。

工作流分为 3 个小工作流：
# indieto_tool_collect (markdown 生成)
1. 用户输入网址，例如 https://jina.ai/，通过 jina reader api 获取官网的基础信息
2. 从网址中获取域名 jina.ai，通过 exa api 在 twitter 搜索产品的特点和用户实际体验等
3. 由 claude 通过 indietool_desc_pattern.md 的提示词整理生成 markdown 文件
4. 点击保存，将 markdown 文件保存到 IndieTO/toolname/desc.md 

# indieto_tool_gen_json (json 生成)
1. 获取上一步保存的 markdown 文件
2. 由 claude 通过 indietool_categorize_pattern.md 的提示词给工具加上分类和标签 slug
3. 由 claude 通过 indietool_json_pattern.md 提示词整理生成 json 文件
4. 点击保存，将 json 文件保存到 IndieTO/toolname/info.json 

# indieto_tool_gen_logo (logo 生成)
1. 输入链接，例如 https://uneed.best/
2. 通过 [img logo API](https://img.logo.dev/uneed.best?token=pk_flBx7FQ8T7i0rIbWfbJgDw&retina=true) 获取网站的 logo 保存到 IndieTO/uneed/logo.jpg 目录下
3. 通过 [apiflash](https://api.apiflash.com/v1/urltoimage?access_key=7716ac4eb9d64fa5911ce98d1bb8fd71&wait_until=page_loaded&url=https://uneed.best/&width=1200&height=1200&no_cookie_banners=true&scroll_page=true&no_ads=true) 获取网站的 screenshot 保存到 IndieTO/uneed/screenshot.jpg 目录下