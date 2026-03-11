import os

# run this .sh will build complete directory structure of the project + initial file content 

project_structure = {
    "datacody-agent": {
        "requirements.txt": "",
        "main.py": "",
        ".env.example": "# 复制此文件为 .env 并填入实际值\nOPENAI_API_KEY=your_key_here",
        "cody_agent": {
            "__init__.py": "",
            "ir": {
                "__init__.py": "", 
                "models.py": ""
            },
            "agent": {
                "__init__.py": "",
                "compiler.py": ""
            },
            "codegen": {
                "__init__.py": "",
                "pandas_generator.py": ""
            },
            "execution": {
                "__init__.py": "", 
                "runner.py": ""
            }
        },
        "test_data": {
            "input.csv": "name,age,email,department\nAlice,28,alice@company.com,Engineering\nBob,35,bob@company.com,Sales\nCharlie,42,charlie@company.com,Engineering\nDiana,23,diana@company.com,Marketing\nEve,31,eve@company.com,Sales",
            ".gitkeep": ""
        },
        "docs": {
            "README.md": "# DataCody Agent\n\n数据工作流编译器",
            "DEVELOPMENT.md": "# 开发指南"
        },
        "tests": {
            "__init__.py": "",
            "test_compiler.py": "",
            "test_codegen.py": ""
        }
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            print(f"创建目录: {path}")
            create_structure(path, content)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"创建文件: {path}")

if __name__ == "__main__":
    base_dir = "."
    create_structure(base_dir, project_structure)
    print("\n✅ 项目结构创建完成！")
