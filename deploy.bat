@echo off
echo Cleaning old package...
rd /s /q backend\lambda\package
del backend\lambda\lambda_deployment.zip

echo Installing dependencies...
pip install -r backend/lambda/requirements.txt -t backend/lambda/package/

echo Copying Lambda code...
copy backend\lambda\handler.py backend\lambda\package\
copy backend\lambda\textract_service.py backend\lambda\package\
copy backend\lambda\bedrock_service.py backend\lambda\package\
copy backend\lambda\s3_service.py backend\lambda\package\

echo Zipping package...
cd backend\lambda\package
powershell Compress-Archive -Path * -DestinationPath ../lambda_deployment.zip
cd C:\Users\shyam\aws-cost-pilot

echo Uploading to Lambda...
aws lambda update-function-code --function-name aws-cost-pilot --zip-file fileb://backend/lambda/lambda_deployment.zip

echo Done! Lambda updated successfully.