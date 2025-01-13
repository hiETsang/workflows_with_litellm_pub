// 监听扩展图标点击事件
chrome.action.onClicked.addListener(async (tab) => {
    console.log('Extension clicked, connecting to native host...');

    try {
        // 连接到本地程序
        const port = chrome.runtime.connectNative('com.indieto.collector');
        console.log('Connected to native host');

        // 设置消息监听器
        port.onMessage.addListener((response) => {
            console.log('Received response:', response);
            if (response.status === 'success') {
                // 等待几秒确保 Streamlit 启动
                setTimeout(() => {
                    console.log('Opening Streamlit with URL:', tab.url);
                    chrome.tabs.create({
                        url: `http://localhost:8501?url=${encodeURIComponent(tab.url)}`
                    });
                }, 3000);
            } else {
                console.error('Error from native host:', response.message);
            }
        });

        // 错误处理
        port.onDisconnect.addListener(() => {
            if (chrome.runtime.lastError) {
                console.error('Native host error:', chrome.runtime.lastError.message);
            }
        });

        // 发送消息给本地程序
        console.log('Sending message to native host');
        port.postMessage({
            action: 'start_streamlit',
            url: tab.url
        });

    } catch (error) {
        console.error('Error connecting to native host:', error);
    }
}); 