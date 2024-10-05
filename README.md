# [Skooldio DEB] Gemini Code Assist for Data Engineering

<p align="center" width="100%">
    <img src="./assets/images/course_title.jpg"> 
</p>

## 🎉 แนะนำตัว
ผู้สอน: ปุณณ์สิริ บุณยเกียรติ (บีท) </br>
Senior Data Engineer, CJ MORE

## 🗓️ สิ่งที่คุณจะได้พบ

ใน Workshop วันนี้เราจะครอบคลุมหัวข้อต่าง ๆ ดังนี้:

### Gemini Code Assist Workshops
1. [What is Gemini and Gemini Code Assist ?]()
2. [Set up local Airflow environment](documents/02_set_up_airflow_env.md)
3. [Set up Gemini Code Assist]()
4. [Explain, generate, complete DAG using prompt]
5. [Prompt Write Doc String]()
6. [Prompt Write Test]()
7. [Prompt to Generate Document Diagram]()
8. [Prompt to Write GE expectation Rule from data]()


### Folder Explaination 
```md
deb-gemini-code-aasist/
│
├── README.md
├── csv_files/
└── dags/
└── runable_dags/
└── documents/
    └── file2.md
```

| Name | Description |
| - | - |
| `dags/` | โฟลเดอร์ที่เก็บโค้ด DAG หรือ Airflow Data Pipelines ที่เราสร้างจะใช้ใน workshop เพื่อทดสอบความสามารถของ Gemini Code Assist |
| `runable_dags/` | โฟลเดอร์ที่เก็บโค้ด DAG หรือ Airflow Data Pipelines ที่เป็นเฉลยของ workshop ใช้งานได้  |
| `docker-compose.yaml` | ไฟล์ Docker Compose ที่ใช้รัน Airflow ขึ้นมาบนเครื่อง |
| `prompts/`| โฟลเดอร์ที่เก็บ prompts ที่ใช้ในการ Generate Code หรือ Query
| `cred/` | โฟลเดอร์ที่เก็บไฟล์ Credential หรือ Configuration อย่างไฟล์ `sa.json` |
