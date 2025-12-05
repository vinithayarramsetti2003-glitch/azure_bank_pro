Azure Banking Data Engineering Project — Day 1

Ingestion Layer setup:
Day 1 focuses on building the Ingestion Layer, the entry point of the Banking Data Platform.
In this layer, every file uploaded to Azure Blob Storage triggers an automated workflow using Event Grid + Azure Functions.

Step 1: Create Azure Storage Account (Raw Zone) & Azure Queue
Azure Storage Account
A dedicated Raw Zone to store all incoming banking files (ATM transactions, UPI transactions, NEFT logs, etc.)
Acts as the first landing area in the data pipeline.
![WhatsApp Image 2025-12-05 at 18 55 52_6cb1737e](https://github.com/user-attachments/assets/1cbd2148-1671-4d47-9b44-eeb0d1e85d33)

Step 2: Deploy Event Grid Trigger Azure Function
I created an Azure Function App, and from my local machine I deployed the EventGridTrigger function.
<img width="1906" height="951" alt="Screenshot 2025-12-05 192544" src="https://github.com/user-attachments/assets/176c38ed-f7c2-4c48-947b-3829dd1644d7" />

Step 3: Configure Event Grid → Azure Function Integration
![WhatsApp Image 2025-12-05 at 20 11 21_f84eaae8](https://github.com/user-attachments/assets/1aa986fb-2167-455f-af5a-eb3a02ad8562)




