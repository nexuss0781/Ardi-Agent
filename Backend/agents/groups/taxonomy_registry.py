# This dictionary represents the full, structured definition of our agent taxonomy.
# It now contains entries for the User Engagement Group and the Analysts Group.

TAXONOMY_REGISTRY = {
    "user_engagement_group": {
        "description": "Handles all initial user interaction, query clarification, and scope definition.",
        "leader": {
            "unique_name": "leader-ueg-gemini-1-5-flash",
            "model_id": "models/gemini-1.5-flash-latest",
            "provider": "Google"
        },
        "labor_model_pools": {
            "Cerebras": ["Llama 4 Scout"],
            "Cohere": ["command-nightly"],
            "Groq": [
                "qwen/qwen3-32b",
                "meta-llama/llama-prompt-guard-2-22m"
            ],
            "Hugging Face": [
                "THUDM/chatglm-6b",
                "meta-llama/Llama-3.1-8B-Instruct"
            ],
            "OpenRouter": [
                "cognitivecomputations/dolphin3.0-mistral-24b:free",
                "google/gemma-3-4b-it:free"
            ],
            "Together AI": [
                "meta-llama/Llama-3-8b-chat-hf",
                "mistralai/Mistral-Small-24B-Instruct-2501"
            ]
        }
    },
    
    "analysts_group": {
        "description": "Handles market research, technical planning, and test case creation.",
        "leader": {
            "unique_name": "leader-analysts-phi-4-reasoning",
            "model_id": "microsoft/phi-4-reasoning-plus:free",
            "provider": "OpenRouter"
        },
        "labor_model_pools": {
            "Cerebras": [
                "Llama 3.3 70B"
            ],
            "Cohere": [
                "command-r"
            ],
            "Google": [
                "models/gemini-1.5-flash-8b-latest"
            ],
            "Groq": [
                "Llama3 70B (8192)",
                "deepseek/deepseek-r1-distill-llama-70b",
                "meta-llama/llama-4-maverick-17b-128e-instruct"
            ],
            "Hugging Face": [
                "tiiuae/falcon-40b-instruct",
                "databricks/dbrx-instruct",
                "nvidia/Nemotron-4-340B-Instruct",
                "tiiuae/falcon-180B-chat",
                "mistralai/Mixtral-8x22B-Instruct-v0.1"
            ],
            "OpenRouter": [
                "nvidia/Llama-3.3-Nemotron-Super-49B-v1:free",
                "shisa-ai/shisa-v2-llama3.3-70b:free",
                "sarvamai/sarvam-m:free",
                "deepseek/deepseek-r1-distill-qwen-32b:free",
                "qwen/qwen3-235b-a22b:free"
            ],
            "Together AI": [
                "meta-llama/Llama-3.3-70B-Instruct-Turbo",
                "arcee-ai/virtuoso-large",
                "Salesforce/Llama-Rank-V1",
                "meta-llama/Llama-3.1-Nemotron-70B-Instruct-HF",
                "lgai/exaone-deep-32b"
            ]
        }
    }
    # ... Other groups will be added here.
}
,
    "innovators_group": {
        "description": "Handles creative brainstorming, feature expansion, and conceptual planning.",
        "leader": {
            "unique_name": "leader-innovators-qwerky-72b",
            "model_id": "featherless/qwerky-72b:free",
            "provider": "OpenRouter"
        },
        "labor_model_pools": {
            "Groq": [
                "llama-3.3-70b-versatile",
                "gemma2-9b-it",
                "compound-beta-mini"
            ],
            "Google": [
                "models/gemini-2.0-flash-exp-image-generation"
            ],
            "Cohere": [
                "c4ai-aya-expanse-32b"
            ],
            "OpenRouter": [
                "tngtech/deepseek-r1t-chimera:free",
                "rekaai/reka-flash-3:free",
                "moonshotai/kimi-vl-a3b-thinking:free",
                "meta-llama/llama-4-maverick:free",
                "mistralai/devstral-small:free",
                "mistralai/mistral-small-3.1-24b-instruct:free"
            ],
            "Hugging Face": [
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "2Noise/ChatTTS",
                "ResembleAl/chatterbox"
            ],
            "Together AI": [
                "deepseek-ai/DeepSeek-V3"
            ]
        }
    }
    
,
    "frontend_development_group": {
        "description": "Handles implementation of user interfaces, including visual components and client-side logic.",
        "leader": {
            "unique_name": "leader-frontend-deepcoder-14b",
            "model_id": "agentica-org/deepcoder-14b-preview:free",
            "provider": "OpenRouter"
        },
        "labor_model_pools": {
            "Cerebras": [
                "Llama 3.1 8B"
            ],
            "Cohere": [
                "c4ai-aya-vision-32b"
            ],
            "Google": [
                "models/gemma-3-12b-it"
            ],
            "Groq": [
                "llama-3.1-8b-instant",
                "allam-2-7b"
            ],
            "Hugging Face": [
                "microsoft/Phi-3-vision-128k-instruct",
                "Qwen/Qwen2-VL-72B-Instruct",
                "timbrooks/instruct-pix2pix",
                "microsoft/Phi-4-multimodal-instruct",
                "microsoft/Phi-3.5-vision-instruct",
                "mistralai/Mistral-Nemo-Instruct-2407",
                "HuggingFaceTB/SmolLM2-1.7B-Instruct",
                "gradientai/Llama-3-8B-Instruct-Gradient-1048k",
                "shenzhi-wang/Llama3-8B-Chinese-Chat",
                "Intel/neural-chat-7b-v3-1",
                "intfloat/e5-mistral-7b-instruct",
                "hkunlp/instructor-xl"
            ],
            "OpenRouter": [
                "opengvlab/internvl3-14b:free",
                "qwen/qwen2.5-vl-32b-instruct:free",
                "qwen/qwen2.5-vl-72b-instruct:free",
                "opengvlab/internvl3-2b:free"
            ],
            "Together AI": [
                "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
                "Qwen/Qwen2.5-VL-72B-Instruct",
                "meta-llama/Llama-Vision-Free",
                "arcee-ai/AFM-4.5B-Preview",
                "arcee-ai/arcee-blitz",
                "arcee-ai/caller",
                "google/gemma-2-27b-it",
                "google/gemma-3n-E4B-it",
                "meta-llama/Llama-3-8B-Instruct-Lite",
                "Qwen/Qwen2.5-7B-Instruct-Turbo",
                "marin-community/marin-8b-instruct",
                "mistralai/Mistral-7B-Instruct-v0.1",
                "mistralai/Mistral-7B-Instruct-v0.2",
                "mistralai/Mistral-7B-Instruct-v0.3",
                "scb10x/scb10x-typhoon-2-1-gemma3-12b",
                "togethercomputer/Refuel-Llm-V2-Small"
            ]
        }
    }
    
,
    "backend_development_group": {
        "description": "Handles implementation of server-side logic, APIs, databases, and system architecture.",
        "leader": {
            "unique_name": "leader-backend-deepseek-coder-v2",
            "model_id": "deepseek-ai/DeepSeek-Coder-V2-Instruct",
            "provider": "Hugging Face"
        },
        "labor_model_pools": {
            "Cohere": [
                "command-r7b-12-2024"
            ],
            "Google": [
                "models/gemma-3-27b-it",
                "google/gemma-3-1b-it"
            ],
            "Groq": [
                "qwen/qwq-32b",
                "compound-beta",
                "meta-llama/llama-4-scout-17b-16e-instruct"
            ],
            "Hugging Face": [
                "microsoft/Phi-3-mini-128k-instruct",
                "meta-llama/Meta-Llama-3-70B-Instruct",
                "THUDM/chatglm3-6b",
                "Qwen/Qwen-7B-Chat",
                "tencent/Hunyuan-A13B-Instruct",
                "TheBloke/Llama-2-13B-chat-GGML",
                "togethercomputer/GPT-NeoXT-Chat-Base-20B",
                "THUDM/glm-4-9b-chat",
                "baichuan-inc/Baichuan-13B-Chat",
                "upstage/SOLAR-10.7B-Instruct-v1.0",
                "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
                "nvidia/Llama3-ChatQA-1.5-8B",
                "microsoft/Phi-4-mini-instruct",
                "mistralai/mistral-small-3.1-24b-instruct-2503",
                "Qwen/Qwen2.5-7B-Instruct",
                "TheBloke/Llama-2-7B-Chat-GGML",
                "mistralai/Mistral-Large-Instruct-2407",
                "meta-llama/Llama-3.1-70B-Instruct",
                "TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF",
                "meta-llama/Llama-2-7b-chat",
                "nvidia/Llama-3.1-Nemotron-70B-Instruct",
                "microsoft/Phi-3.5-MoE-instruct"
            ],
            "OpenRouter": [
                "thudm/glm-z1-32b:free",
                "deepseek/deepseek-r1-0528-qwen3-8b:free",
                "Qwen/Qwen3-8B (free)",
                "Qwen/Qwen3-14B (free)",
                "Qwen/Qwen3-32B (free)",
                "Qwen/Qwen3-30B-A3B (free)",
                "qwen/qwq-32b:free",
                "microsoft/mai-ds-r1:free",
                "mistralai/mistral-small-24b-instruct-2501",
                "mistralai/mistral-small-3.2-24b-instruct:free",
                "moonshotai/kimi-dev-72b:free",
                "nousresearch/deephermes-3-llama-3-8b-preview:free",
                "mistralai/mistral-small-3.1-24b-instruct:free"
            ],
            "Together AI": [
                "deepseek-ai/DeepSeek-R1",
                "deepseek-ai/DeepSeek-R1-0528-tput",
                "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
                "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
                "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
                "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
                "lgai/exaone-3-5-32b-instruct",
                "meta-llama/Llama-2-70b-hf",
                "meta-llama/Llama-3-70b-chat-hf",
                "meta-llama/Llama-3.2-3B-Instruct-Turbo",
                "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
                "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
                "meta-llama/Llama-4-Scout-17B-16E-Instruct",
                "meta-llama/Meta-Llama-3-8B-Instruct-Lite",
                "meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
                "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
                "Qwen/QwQ-32B",
                "Qwen/Qwen2-72B-Instruct",
                "Qwen/Qwen2.5-72B-Instruct-Turbo",
                "Qwen/Qwen3-235B-A22B-fp8-tput",
                "perplexity-ai/r1-1776",
                "togethercomputer/Refuel-Llm-V2",
                "scb10x/scb10x-llama3-1-typhoon2-70b-instruct",
                "arcee-ai/virtuoso-medium-v2",
                "arcee-ai/coder-large"
            ]
        }
    }
    
,
    "debugging_support_group": {
        "description": "Handles bug identification, code correction, and providing support for implemented features.",
        "leader": {
            "unique_name": "leader-debugging-maestro-reasoning",
            "model_id": "arcee-ai/maestro-reasoning",
            "provider": "Together AI"
        },
        "labor_model_pools": {
            "Cohere": [
                "command-light-nightly"
            ],
            "Google": [
                "models/gemini-2.5-flash-preview-04-17-thinking"
            ],
            "Groq": [
                "llama3-8b-8192"
            ],
            "Hugging Face": [
                "meta-llama/Llama-3.2-1B-Instruct",
                "tiiuae/falcon-7b-instruct",
                "meta-llama/Llama-3.2-3B-Instruct",
                "meta-llama/Llama-2-13b-chat-hf",
                "Qwen/Qwen2.5-72B-Instruct",
                "microsoft/Phi-3.5-mini-instruct",
                "meta-llama/Llama-2-7b-chat-hf",
                "mistralai/Mistral-7B-Instruct-v0.2",
                "THUDM/chatglm2-6b",
                "mistralai/Mistral-7B-Instruct-v0.3",
                "mistralai/Mistral-7B-Instruct-v0.1",
                "microsoft/Phi-3-mini-4k-instruct",
                "meta-llama/Llama-3.3-70B-Instruct"
            ],
            "OpenRouter": [
                "deepseek/deepseek-v3-base:free",
                "thudm/glm-4-32b:free",
                "cognitivecomputations/dolphin3.0-r1-mistral-24b:free",
                "deepseek/deepseek-chat-v3-0324:free"
            ],
            "Together AI": [
                "arcee_ai/arcee-spotlight"
            ]
        }
    }
    
,
    "qa_council": {
        "description": "Handles all quality assurance, testing, and evaluation of plans and code. Composed of specialized sub-groups.",
        "sub_groups": {
            "code_quality_auditor": {
                "description": "Audits code for style, standards, and best practices.",
                "leader": {
                    "unique_name": "leader-qa-code-qwen-coder",
                    "model_id": "Qwen/Qwen2.5-Coder-32B-Instruct",
                    "provider": "Hugging Face"
                },
                "labor_model_pools": {
                    "Together AI": ["deepseek-ai/DeepSeek-R1-0528-tput"]
                }
            },
            "security_auditor": {
                "description": "Scans for security vulnerabilities and unsafe practices.",
                "leader": {
                    "unique_name": "leader-qa-security-prompt-guard",
                    "model_id": "meta-llama/llama-prompt-guard-2-86m",
                    "provider": "Groq"
                },
                "labor_model_pools": {
                    "Together AI": ["meta-llama/Llama-Guard-3-11B-Vision-Turbo"]
                }
            },
            "performance_auditor": {
                "description": "Checks for performance bottlenecks and inefficient code.",
                "leader": {
                    "unique_name": "leader-qa-performance-phi-4-reasoning",
                    "model_id": "microsoft/phi-4-reasoning:free",
                    "provider": "OpenRouter"
                },
                "labor_model_pools": {
                    "Hugging Face": ["meta-llama/Llama-4-Scout-17B-16E-Instruct"]
                }
            },
            "ux_logic_auditor": {
                "description": "Verifies that the output aligns with the project brief's user experience and logic.",
                "leader": {
                    "unique_name": "leader-qa-ux-gemini-1-5-flash",
                    "model_id": "models/gemini-1.5-flash-002",
                    "provider": "Google"
                },
                "labor_model_pools": {
                    "Cohere": ["command-r-plus-08-2024"]
                }
            },
            "antagonistic_tester": {
                "description": "Acts as a red team to find edge cases and logical flaws.",
                "leader": {
                    "unique_name": "leader-qa-red-team-arliai",
                    "model_id": "arliai/qwq-32b-arliai-rpr-v1:free",
                    "provider": "OpenRouter"
                },
                "labor_model_pools": {
                    "Hugging Face": ["NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"]
                }
            }
        }
    }

,
    "language_expert_group": {
        "description": "A specialist group responsible for grammatical and semantic polishing of the user's initial query.",
        "leader": {
            "unique_name": "leader-lang-expert-gemini-1-5-flash",
            "model_id": "models/gemini-1.5-flash-latest",
            "provider": "Google"
        },
        "labor_model_pools": {}
    }
    
,
    "adjudication_unit": {
        "description": "Acts as the final, impartial decider in disputes between Supervisors and Evaluators to prevent deadlocks.",
        "leader": {
            "unique_name": "leader-justifier-llama-3-1-405b",
            "model_id": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            "provider": "Together AI"
        },
        "labor_model_pools": {}
    }
}