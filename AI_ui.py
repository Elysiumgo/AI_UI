import os
import openai
import gradio as gr

# ... (保留你的 API Key 和 MODEL_CONFIGS 定义) ...

# 核心交互函数：增加了 top_p 参数并修复了智谱报错问题
def interact_llm(chatbot, user_input, model_choice, temp, top_p):
    if not user_input:
        return chatbot, ""
    
    try:
        config = MODEL_CONFIGS[model_choice]
        client = openai.OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )

        # 1. 构造消息历史 (确保格式兼容)
        messages = []
        for msg in chatbot:
            if isinstance(msg, dict):
                messages.append(msg)
            else:
                messages.append({"role": "user", "content": msg[0]})
                messages.append({"role": "assistant", "content": msg[1]})
        messages.append({"role": "user", "content": user_input})

        # 2. 【解决智谱报错】对温度进行参数校验
        current_temp = float(temp)
        if model_choice == "智谱AI-ChatGLM":
            # 智谱要求 (0, 1.0]，我们限制在 0.01 到 0.99 之间最稳
            current_temp = max(0.01, min(0.99, current_temp))
        
        # 3. 调用 API (加入了 top_p)
        response = client.chat.completions.create(
            model=config["model"],
            messages=messages,
            temperature=current_temp,
            top_p=float(top_p) 
        )
        
        bot_reply = response.choices[0].message.content

        # 4. 更新界面
        chatbot.append({"role": "user", "content": user_input})
        chatbot.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        chatbot.append({"role": "assistant", "content": f"发生错误：{str(e)}"})
    
    return chatbot, ""

# --- 界面部分 ---
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 HCI Lab 2: Multi-Model Comparison")
    
    with gr.Row():
        with gr.Column(scale=1):
            model_selector = gr.Dropdown(
                choices=list(MODEL_CONFIGS.keys()), 
                value="阿里云-通义千问", 
                label="选择模型"
            )
            # 两个核心滑块
            temp_slider = gr.Slider(0, 2, 1, step=0.1, label="温度 (Temperature)")
            top_p_slider = gr.Slider(0, 1.0, 0.7, step=0.05, label="核采样阈值 (Top-p)")
            
            reset_btn = gr.Button("🗑️ 清空对话")
        
        with gr.Column(scale=3):
            chatbot_ui = gr.Chatbot(label="聊天窗口") 
            msg_input = gr.Textbox(placeholder="输入问题并回车...", label="输入框")
            send_btn = gr.Button("🚀 发送", variant="primary")

    # 事件绑定 (注意 inputs 列表里增加了 top_p_slider)
    send_btn.click(
        interact_llm, 
        inputs=[chatbot_ui, msg_input, model_selector, temp_slider, top_p_slider], 
        outputs=[chatbot_ui, msg_input]
    )
    msg_input.submit(
        interact_llm, 
        inputs=[chatbot_ui, msg_input, model_selector, temp_slider, top_p_slider], 
        outputs=[chatbot_ui, msg_input]
    )
    reset_btn.click(lambda: [], None, chatbot_ui)

if __name__ == "__main__":
    demo.launch(debug=True)