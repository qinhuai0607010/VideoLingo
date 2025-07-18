# from pathlib import Path
# # Import IndexTTS class from the index-tts project
# # Make sure the directory containing index-tts is in Python's sys.path
# try:
#     from indextts.infer import IndexTTS
# except ImportError:
#     print("Error: Could not import IndexTTS. Please ensure the index-tts directory is in Python's sys.path.")
#     IndexTTS = None # Set to None if import fails

# # Import load_config to read from config.yaml
# try:
#     # from core.config import load_config
#     from core.utils.config_utils import load_key
#     print('成功导入load_key')

# except ImportError:
#     print("Error: Could not import load_config from core.config.")
#     load_config = None

# import os # Import os for path checking

# # Read configuration from config.yaml and initialize IndexTTS model
# tts_model = None
# INDEX_TTS_REFERENCE_VOICE_PATH = None

# if IndexTTS:
#     INDEX_TTS_CONFIG = load_key('index_tts')
#     INDEX_TTS_MODEL_DIR = INDEX_TTS_CONFIG.get('model_dir')
#     INDEX_TTS_CFG_PATH = INDEX_TTS_CONFIG.get('cfg_path')
#     INDEX_TTS_REFERENCE_VOICE_PATH = INDEX_TTS_CONFIG.get('reference_voice_path')

#     if INDEX_TTS_MODEL_DIR and INDEX_TTS_CFG_PATH:
#         try:
#             # Initialize IndexTTS model once when the module is loaded
#             tts_model = IndexTTS(model_dir=INDEX_TTS_MODEL_DIR, cfg_path=INDEX_TTS_CFG_PATH)
#             print("IndexTTS model initialized successfully.")
#         except Exception as e:
#             print(f"Error initializing IndexTTS model with paths {INDEX_TTS_MODEL_DIR}, {INDEX_TTS_CFG_PATH}: {e}")
#     else:
#         print("IndexTTS model_dir or cfg_path not found in config.yaml. IndexTTS will not be available.")
# elif not load_config:
#     print("Configuration loader not available. Cannot load IndexTTS settings.")
# elif not IndexTTS:
#      print("IndexTTS class not available due to import error.")


# def custom_tts(text, save_path):
#     """
#     Custom TTS (Text-to-Speech) interface using IndexTTS

#     Args:
#         text (str): Text to be converted to speech
#         save_path (str): Path to save the audio file

#     Returns:
#         None

#     Example:
#         custom_tts("Hello world", "output.wav")
#     """
#     # Check if the model was successfully initialized
#     if tts_model is None:
#         print("IndexTTS model not initialized. Cannot perform TTS.")
#         # Depending on desired behavior, you might raise an exception here
#         return

#     # Check if reference voice path is configured and exists
#     if not INDEX_TTS_REFERENCE_VOICE_PATH or not os.path.exists(INDEX_TTS_REFERENCE_VOICE_PATH):
#         print(f"Reference voice path is not configured or file not found: {INDEX_TTS_REFERENCE_VOICE_PATH}. Cannot perform TTS.")
#         # Depending on desired behavior, you might raise an exception here
#         return

#     # Ensure save directory exists
#     speech_file_path = Path(save_path)
#     speech_file_path.parent.mkdir(parents=True, exist_ok=True)

#     try:
#         # TODO: Implement your custom TTS logic here
#         # 1. Initialize your TTS client/model (Done outside the function)
#         # 2. Convert text to speech
#         # Use the initialized IndexTTS model to perform inference
#         tts_model.infer(INDEX_TTS_REFERENCE_VOICE_PATH, text, save_path)
#         # 3. Save the audio file to the specified path (Done by tts_model.infer)

#         print(f"Audio saved to {speech_file_path}")
#     except Exception as e:
#         print(f"Error occurred during IndexTTS conversion for text '{text[:50]}...': {str(e)}")
#         # Optionally re-raise the exception if it should stop processing
#         # raise


# if __name__ == "__main__":
#     # Test example
#     # For this test to work, ensure config.yaml has the 'index_tts' section
#     # with valid 'model_dir', 'cfg_path', and 'reference_voice_path',
#     # and that the index-tts directory is in sys.path.
#     print("Running custom_tts (IndexTTS) test...")
#     test_text = "这是一个使用 IndexTTS 进行自定义语音合成的测试。"
#     test_save_path = "custom_tts_index_tts_test_output.wav"

#     # Ensure the test directory exists
#     os.makedirs(os.path.dirname(test_save_path) or '.', exist_ok=True)

#     custom_tts(test_text, test_save_path)
#     print(f"Test finished. Check for {test_save_path}")



# custom_tts.py

from pathlib import Path
import os
import sys
import torch
import torchaudio



# --- 关键路径设置：处理 Matcha-TTS 依赖 ---
# 直接使用您指定的项目文件夹路径 /CosyVoice

# 1. 定义项目根目录的绝对路径
cosyvoice_project_path = '/content/CosyVoice'
matcha_tts_path = os.path.join(cosyvoice_project_path, '/content/CosyVoice/third_party/Matcha-TTS')

# 2. 检查核心路径是否存在，如果不存在则提供清晰的错误信息
if not os.path.isdir(cosyvoice_project_path):
    print("="*60)
    print(f"!! 严重错误: CosyVoice 项目目录未找到 !!")
    print(f"代码中设定的固定路径是: '{cosyvoice_project_path}'")
    print("请确认您的 CosyVoice 项目文件夹是否真的位于这个位置，并且名称大小写完全匹配。")
    print("="*60)
    # 后续的导入很可能会失败
else:
    print(f"已确认 CosyVoice 项目目录存在: '{cosyvoice_project_path}'")

# 3. 将必要的路径添加到 sys.path 以确保模块可以被导入
#    使用 insert(0, ...) 确保最高导入优先级，避免潜在的模块冲突。

# 添加 Matcha-TTS 依赖路径
if matcha_tts_path not in sys.path:
    # 检查子目录是否存在
    if os.path.isdir(matcha_tts_path):
        sys.path.insert(0, matcha_tts_path)
        print(f"成功将 Matcha-TTS 路径添加到 sys.path: '{matcha_tts_path}'")
    else:
        print(f"!! 错误: 在 '{cosyvoice_project_path}' 中未找到 'third_party/Matcha-TTS' 子目录。")

# 添加 CosyVoice 项目根目录（尽管主调用脚本应该已经做了，但这是双重保险）
if cosyvoice_project_path not in sys.path:
    sys.path.insert(0, cosyvoice_project_path)
    print(f"成功将 CosyVoice 根目录添加到 sys.path: '{cosyvoice_project_path}'")


# --- 导入 CosyVoice ---
# (这部分及之后的所有代码保持不变)
try:
    from cosyvoice.cli.cosyvoice import CosyVoice2
    from cosyvoice.utils.file_utils import load_wav
    # from cosyvoice.utils.common import set_all_random_seed
    # from cosyvoice.vllm.cosyvoice2 import CosyVoice2ForCausalLM
    # ModelRegistry.register_model("CosyVoice2ForCausalLM", CosyVoice2ForCausalLM)
    print("成功导入 CosyVoice2 模块。")
except ImportError as e:
    print(f"错误: 无法导入 CosyVoice2。请确保 cosyvoice 及其依赖已正确安装。 {e}")
    CosyVoice2 = None
    load_wav = None

# --- 导入 VideoLingo 配置加载工具 ---
try:
    from core.utils.config_utils import load_key
    print('成功导入 load_key。')
except ImportError:
    print("错误: 无法从 core.utils.config_utils 导入 load_key。")
    load_key = None

# --- 初始化 CosyVoice 模型和参考音频 (一次性加载) ---
tts_model = None
PROMPT_TEXT = None
PROMPT_SPEECH_16K = None

if CosyVoice2 and load_key and load_wav:
    COSYVOICE_CONFIG = load_key('cosyvoice')
    COSYVOICE_MODEL_DIR = COSYVOICE_CONFIG.get('model_dir')
    COSYVOICE_PROMPT_WAV_PATH = COSYVOICE_CONFIG.get('prompt_wav_path')
    PROMPT_TEXT = COSYVOICE_CONFIG.get('prompt_text')

    if all([COSYVOICE_MODEL_DIR, COSYVOICE_PROMPT_WAV_PATH, PROMPT_TEXT]):
        try:
            if not os.path.exists(COSYVOICE_PROMPT_WAV_PATH):
                raise FileNotFoundError(f"指定的参考音频文件不存在: {COSYVOICE_PROMPT_WAV_PATH}")

            # 检查是否有可用的 GPU
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"CosyVoice 将使用设备: {device}")

            # 1. 初始化 CosyVoice2 模型
            # 注意：这里的参数可以根据你的硬件进行调整
            tts_model = CosyVoice2(COSYVOICE_MODEL_DIR, load_jit=False, load_trt=False, load_vllm=False, fp16=False)

            # tts_model = CosyVoice2(COSYVOICE_MODEL_DIR, load_jit=True, load_trt=True, load_vllm=True, fp16=True)

            print("CosyVoice2 模型初始化成功。")

            # 2. 加载参考音频并重采样到 16k
            PROMPT_SPEECH_16K = load_wav(COSYVOICE_PROMPT_WAV_PATH, 16000)
            print(f"成功加载参考音频: {COSYVOICE_PROMPT_WAV_PATH}")

        except Exception as e:
            print(f"初始化 CosyVoice 或加载参考音频时出错: {e}")
            tts_model = None # 确保在出错时模型为 None
            import traceback
            traceback.print_exc()
    else:
        print("在 config.yaml 中 'cosyvoice' 配置不完整。需要 'model_dir', 'prompt_wav_path', 和 'prompt_text'。")
else:
    if not CosyVoice2:
        print("CosyVoice2 类因导入错误而不可用。")
    if not load_key:
        print("配置加载器不可用，无法加载 CosyVoice 设置。")


def custom_tts(text: str, save_path: str):
    """
    使用 CosyVoice2 的零样本(zero-shot)接口进行自定义文本转语音

    Args:
        text (str): 要转换为语音的目标文本。
        save_path (str): 保存输出音频文件的路径。
    """
    if tts_model is None or PROMPT_SPEECH_16K is None:
        print("CosyVoice 模型或参考音频未成功初始化。无法执行 TTS。")
        return

    # 确保保存目录存在
    speech_file_path = Path(save_path)
    speech_file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        print(f"使用零样本克隆技术生成音频: '{text[:40]}...'")

        # 调用 inference_zero_shot 函数
        # 它返回一个生成器，我们只取第一个结果
        # output_generator = tts_model.inference_zero_shot(
        #     text,
        #     PROMPT_TEXT,
        #     PROMPT_SPEECH_16K,
        #     stream=False # 设置为 False 以一次性获取完整音频
        # )

        output_generator = tts_model.inference_instruct2(text, '用粤语说这句话', PROMPT_SPEECH_16K, stream=False)
        
        # 从生成器中获取第一个（也可能是唯一一个）结果
        result = next(output_generator, None)

        if result and 'tts_speech' in result:
            # 保存音频文件
            torchaudio.save(
                str(speech_file_path),
                result['tts_speech'],
                tts_model.sample_rate
            )
            print(f"音频成功保存到 {speech_file_path}")
        else:
            print(f"错误: CosyVoice2 未能为文本 '{text[:50]}...' 生成音频。")

    except Exception as e:
        print(f"为文本 '{text[:50]}...' 进行 CosyVoice 转换时发生严重错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # --- 测试示例 ---
    # 要使此测试正常工作，请确保:
    # 1. 你已在 cosyvoice 环境中运行此脚本。
    # 2. VideoLingo 的根目录是当前工作目录，或能够找到 config.yaml。
    # 3. 在 VideoLingo/config/config.yaml 中已正确配置 'cosyvoice' 部分。

    print("\n" + "="*50)
    print("运行 custom_tts (CosyVoice2 Zero-Shot) 测试...")
    
    # 模拟从 VideoLingo 根目录运行，以便能找到配置文件
    if os.path.basename(os.getcwd()) != 'VideoLingo':
        # 假设项目文件夹名为 VideoLingo
        if os.path.exists('../VideoLingo'):
            os.chdir('../VideoLingo')
        elif os.path.exists('/VideoLingo'):
            os.chdir('/VideoLingo')
    print(f"当前工作目录: {os.getcwd()}")


    test_text_mandarin = "这是一个使用 CosyVoice 进行零样本音色克隆的测试。"
    test_text_cantonese = '收到朋友由好遠寄嚟嘅生日禮物，嗰份意外嘅驚喜同深深嘅祝福，令我個心充滿咗甜蜜嘅快樂。'
    test_save_path = "output/custom_tts_cosyvoice2_test_output.wav"
    
    # 确保测试目录存在
    os.makedirs(os.path.dirname(test_save_path), exist_ok=True)
    
    # 使用配置中设定的参考音色，合成普通话文本
    custom_tts(test_text_mandarin, test_save_path)
    
    print(f"\n测试完成。请检查文件: {test_save_path}")
    print("注意：输出的语言和音色取决于你的目标文本以及在 config.yaml 中配置的参考音频和提示文本。")
    print("="*50 + "\n")