import streamlit as st
import subprocess
import tempfile
import os
from dotenv import load_dotenv
import yaml

# Load environment variables
load_dotenv()

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# 初始化session state
if 'workflow_state' not in st.session_state:
    st.session_state.workflow_state = {
        'current_workflow': 'indieto_tool_collect',  # 设置默认工作流
        'output_content': None,
        'input_content': None,  # 添加输入内容的状态
        'workflow_sequence': [
            'indieto_tool_collect',
            'indieto_tool_gen_json',
            'indieto_tool_gen_logo',
            'indieto_tool_upload'
        ],
        'switching_workflow': False  # 添加这个标志
    }

def get_next_workflow(current_workflow):
    """获取下一个工作流"""
    sequence = st.session_state.workflow_state['workflow_sequence']
    try:
        current_index = sequence.index(current_workflow)
        if current_index < len(sequence) - 1:
            return sequence[current_index + 1]
    except ValueError:
        pass
    return None

def switch_to_next_workflow():
    """切换到下一个工作流"""
    current = st.session_state.workflow_state['current_workflow']
    next_workflow = get_next_workflow(current)
    if next_workflow:
        # 设置切换标志
        st.session_state.workflow_state['switching_workflow'] = True
        # 保存当前输出作为下一步的输入
        st.session_state.workflow_state['previous_output'] = st.session_state.workflow_state.get('output_content')
        # 清除当前保存的输入内容
        st.session_state.workflow_state['input_content'] = None
        # 更新当前工作流
        st.session_state.workflow_state['current_workflow'] = next_workflow
        # 清除输出内容
        st.session_state.workflow_state['output_content'] = None

def create_api_key_input(key_name, env_var_name):
    """创建API key输入框并处理其逻辑"""
    # 直接从.env文件读取值
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    env_value = ""
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip().startswith(f"{env_var_name} ="):
                    env_value = line.split('=')[1].strip()
                    break
    
    # 创建密码输入框
    api_key = st.text_input(
        f"{key_name} API Key", 
        value=env_value,
        type="password",
        help=f"Enter your {key_name} API key"
    )
    
    # 如果用户输入了新的API key且与环境变量不同
    if api_key and api_key != env_value:
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            # 查找并更新API key
            key_found = False
            for i, line in enumerate(lines):
                if line.strip().startswith(f"{env_var_name} ="):
                    lines[i] = f"{env_var_name} = {api_key}\n"
                    key_found = True
                    break
            
            if not key_found:
                lines.append(f"{env_var_name} = {api_key}\n")
            
            # 写入更新后的内容
            with open(env_path, 'w') as f:
                f.writelines(lines)
        else:
            # 如果.env文件不存在，创建新文件
            with open(env_path, 'w') as f:
                f.write(f"{env_var_name} = {api_key}\n")
        
        # 更新环境变量
        os.environ[env_var_name] = api_key
    
    return api_key

def load_workflows():
    workflows = []
    config_dir = os.path.join(current_dir, 'config')
    for file in os.listdir(config_dir):
        if file.endswith('.yaml'):
            workflows.append(file.replace('.yaml', ''))
    return workflows

def load_config(workflow):
    config_path = os.path.join(current_dir, 'config', f'{workflow}.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# Streamlit app
st.title('IndieTO工具收集工作流')

# API Keys section in sidebar
with st.sidebar:
    st.header('API Keys')
    openrouter_api_key = create_api_key_input("OpenRouter", "OPENROUTER_API_KEY")
    exa_api_key = create_api_key_input("EXA", "EXA_API_KEY")
    apiflash_key = create_api_key_input("APIFlash", "APIFLASH_KEY")
    
    # 添加OpenAI设置
    st.subheader('OpenAI Settings')
    openai_api_key = create_api_key_input("OpenAI", "OPENAI_API_KEY")
    
    # 从.env文件读取 OPENAI_API_BASE
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    env_base_url = ""
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip().startswith('OPENAI_API_BASE ='):
                    env_base_url = line.split('=')[1].strip()
                    break
    
    openai_api_base = st.text_input(
        "OpenAI API Base URL",
        value=env_base_url,
        help="Enter your OpenAI API base URL (optional)"
    )
    
    if openai_api_base and openai_api_base != env_base_url:
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            base_found = False
            for i, line in enumerate(lines):
                if line.strip().startswith("OPENAI_API_BASE ="):
                    lines[i] = f"OPENAI_API_BASE = {openai_api_base}\n"
                    base_found = True
                    break
            
            if not base_found:
                lines.append(f"OPENAI_API_BASE = {openai_api_base}\n")
            
            with open(env_path, 'w') as f:
                f.writelines(lines)
        else:
            with open(env_path, 'w') as f:
                f.write(f"OPENAI_API_BASE = {openai_api_base}\n")
        
        os.environ["OPENAI_API_BASE"] = openai_api_base

# 工作流进度显示
st.write("工作流程：")
workflow_sequence = st.session_state.workflow_state['workflow_sequence']
current_workflow = st.session_state.workflow_state['current_workflow']

# 显示工作流进度
cols = st.columns(len(workflow_sequence))
for i, workflow in enumerate(workflow_sequence):
    with cols[i]:
        if workflow == current_workflow:
            st.markdown(f"**[{workflow}]**")
        elif workflow in st.session_state.workflow_state['workflow_sequence'][:workflow_sequence.index(current_workflow) if current_workflow else 0]:
            st.markdown(f"~~{workflow}~~")
        else:
            st.markdown(workflow)

# Workflow selection
workflows = load_workflows()
# 使用 session state 来存储选择的工作流
if st.session_state.workflow_state.get('switching_workflow'):
    # 重置切换标志
    st.session_state.workflow_state['switching_workflow'] = False
    # 强制选择新的工作流
    selected_workflow = st.session_state.workflow_state['current_workflow']
else:
    # 正常的工作流选择逻辑
    workflows = load_workflows()
    selected_workflow = st.selectbox(
        '选择工作流', 
        workflows,
        index=workflows.index(st.session_state.workflow_state['current_workflow'])
    )

if selected_workflow != st.session_state.workflow_state['current_workflow'] and not st.session_state.workflow_state.get('switching_workflow'):
    st.session_state.workflow_state['current_workflow'] = selected_workflow
    st.session_state.workflow_state['output_content'] = None
    st.session_state.workflow_state['input_content'] = None  # 清除保存的输入内容
    st.rerun()

# Load config for selected workflow
config = load_config(selected_workflow)

# 根据工作流显示不同的输入提示
input_prompts = {
    'indieto_tool_collect': '请输入要收集的工具网址',
    'indieto_tool_gen_json': '请输入工具描述markdown',
    'indieto_tool_gen_logo': '请输入工具JSON',
    'indieto_tool_upload': '请输入JSON文件路径'
}

# Text input
if 'previous_output' in st.session_state.workflow_state and st.session_state.workflow_state['previous_output']:
    # 使用 previous_output 作为初始值，并同时更新 input_content
    initial_value = st.session_state.workflow_state['previous_output']
    st.session_state.workflow_state['input_content'] = initial_value
    # 清除 previous_output，避免重复使用
    st.session_state.workflow_state['previous_output'] = None
elif st.session_state.workflow_state.get('input_content') is not None:
    # 如果有保存的输入内容，使用它
    initial_value = st.session_state.workflow_state['input_content']
else:
    initial_value = ""

def update_input():
    st.session_state.workflow_state['input_content'] = st.session_state.input_text

input_text = st.text_area(
    input_prompts.get(selected_workflow, '输入文本'),
    value=initial_value,
    height=200,
    key='input_text',
    on_change=update_input
)

# Process button
if st.button('处理'):
    if input_text:
        # 确保当前输入内容被保存
        st.session_state.workflow_state['input_content'] = input_text
        with st.spinner('处理中...'):
            # Save input text to a temporary file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as temp_file:
                temp_file.write(input_text)
                temp_file_path = temp_file.name

            # Prepare command with full path to app.py
            app_path = os.path.join(current_dir, 'app.py')
            cmd = ['poetry', '--directory', current_dir, 'run', 'python', app_path, temp_file_path, '--workflow', selected_workflow]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                
                # Display output and provide download link
                output_file = os.path.join(os.path.dirname(temp_file_path), f'{selected_workflow}-output.md')
                if os.path.exists(output_file):
                    with open(output_file, 'r', encoding='utf-8') as f:
                        output_content = f.read()
                    
                    # 显示输出结果
                    output_container = st.container()
                    with output_container:
                        st.text_area('输出结果', output_content, height=300)
                        st.download_button('下载输出结果', output_content, file_name=f'{selected_workflow}-output.md')
                    
                    # 保存输出结果到状态
                    st.session_state.workflow_state['output_content'] = output_content
                    
                    # 获取下一个工作流
                    next_workflow = get_next_workflow(selected_workflow)
                    if next_workflow:
                        col1, col2 = st.columns([1, 5])
                        with col1:
                            if st.button('继续下一步', key='next_step', on_click=switch_to_next_workflow):
                                st.rerun()
                        with col2:
                            st.info(f'点击继续将进入: {next_workflow}')
                else:
                    st.warning('未找到输出文件。显示标准输出和错误信息用于调试：')
                    st.text_area('标准输出', result.stdout, height=300)
                    if result.stderr:
                        st.text_area('标准错误', result.stderr, height=300)

            except subprocess.CalledProcessError as e:
                st.error(f'发生错误。显示标准输出和错误信息用于调试：')
                st.text_area('标准输出', e.stdout, height=300)
                st.text_area('标准错误', e.stderr, height=300)

            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
    else:
        st.warning('请输入要处理的文本。')

# 重置按钮
if st.button('重新开始'):
    st.session_state.workflow_state = {
        'current_workflow': 'indieto_tool_collect',
        'output_content': None,
        'previous_output': None,
        'workflow_sequence': workflow_sequence
    }
    st.rerun()
