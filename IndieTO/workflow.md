背景：开发并且上线了一个导航站，基于 mkdirs 模版，后台使用 sanity 管理，但是 sanity 上传数据太慢了，手动一个个传操作不方便，并且不支持批量上传。
目前工作流构思如下：
最终实现的效果：
打开 web 页面输入域名，经过联网收集和 AI 处理之后，在 IndieTO 目录下得到一个工具详情页内容的 markdown 文件，以及 可以通过接口上传到 sanity后台的 json 文件，以及网站的 logo 和 screenshot。一共四个文件。
工作流：
当前的项目基于当前项目 python 脚本，并且通过 Streamlit 生成 web 网站。
1. 用户输入网址，例如https://jina.ai/，通过 jina reader 获取官网的基础信息
2. 从网址中获取域名 jina.ai，通过 exa 在 twitter 搜索产品的特点和用户实际体验等
3. 由 claude 通过 indietool_desc_pattern 整理生成 markdown 文件
4. 将 markdown 文件显示在 MarkdownOutput 中，用户可以编辑，下方显示下一步按钮，点击继续执行下一步
5. 由 claude 通过 indietool_categorize_pattern 的分类和标签给工具加上分类和标签 slug
6. 由 claude 通过 indietool_json_pattern 整理生成 json 文件，将 json 文件显示在 JsonOutput 中，用户可以编辑，下方显示一个 save 按钮，点击网页中的 save，执行后续保存的7-10步
7. 将生成的 markdown 保存到 IndieTO/toolname/desc.md 
8. 将生成的 json 文件保存到 IndieTO/toolname/info.json 
9. 通过 [jina reader](https://img.logo.dev/mcdonalds.com?token=pk_flBx7FQ8T7i0rIbWfbJgDw&retina=true) 获取网站的 logo 保存到 IndieTO/toolname/logo.jpg 目录下
10. 通过 [apiflash](https://api.apiflash.com/v1/urltoimage?access_key=7716ac4eb9d64fa5911ce98d1bb8fd71&wait_until=page_loaded&url=http://cursor.com&width=1200&height=1200&no_cookie_banners=true&scroll_page=true&no_ads=true) 获取网站的 screenshot 保存到 IndieTO/toolname/screenshot.jpg 目录下



