import {getRequest, postRequest} from "../httpclient/httpclient";

// 定义formData初始状态 shape
export const initialFormData = {
    "liveStreamingConfig": {
        "B_ROOM_ID": "27892212",
        "B_COOKIE": ""
    },
    "enableProxy": false,
    "enableLive": false,
    "httpProxy": "http://host.docker.internal:23457",
    "httpsProxy": "https://host.docker.internal:23457",
    "socks5Proxy": "socks5://host.docker.internal:23457",
    "languageModelConfig": {
        "openai": {
            "MODEL_NAME": "gpt-3.5-turbo",
            "OPENAI_API_KEY": "sk-",
            "OPENAI_BASE_URL": ""
        },
        "ollama": {
            "OLLAMA_API_BASE": "http://localhost:11434",
            "OLLAMA_API_MODEL_NAME": "qwen:7b"
        },
        "zhipuai":  {
            "ZHIPUAI_API_KEY": "sk"
        }
    },
    "characterConfig": {
        "character": 1,
        "character_name": "爱莉",
        "yourName": "yuki129",
        "vrmModel": "\u308f\u305f\u3042\u3081_03.vrm",
        "vrmModelType": "system"
    },
    "conversationConfig": {
        "conversationType": "default",
        "languageModel": "openai"
    },
    "memoryStorageConfig": {
        "milvusMemory": {
            "host": "127.0.0.1",
            "port": "19530",
            "user": "user",
            "password": "Milvus",
            "dbName": "default"
        },
        "zep_memory": {
            "zep_url": "http://localhost:8881",
            "zep_optional_api_key": "optional_api_key"
        },
        "enableLongMemory": false,
        "enableSummary": false,
        "languageModelForSummary": "openai",
        "enableReflection": false,
        "languageModelForReflection": "openai"
    },
    "custom_role_template_type": "zh",
    "background_id": 1,
    "background_url": "",
    "ttsConfig": {
        "ttsType": "Edge",
        "ttsVoiceId": "zh-CN-XiaoyiNeural"
    }
}

// 定义类型别名
export type GlobalConfig = typeof initialFormData;

export async function getConfig() {

    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };

    const chatRes = await getRequest("/chatbot/config/get", headers);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }

    return chatRes.response;
}

export async function saveConfig(
    config: Object
) {

    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };

    const body = {
        "config": config
    };

    const chatRes = await postRequest("/chatbot/config/save", headers, body);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }

    return chatRes.response;
}