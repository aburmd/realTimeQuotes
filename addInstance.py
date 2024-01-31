import boto3

# Your bootstrap script
user_data_script = "IyEvYmluL2Jhc2gKY3VybCAtTyBodHRwczovL2Jvb3RzdHJhcC5weXBhLmlvL2dldC1waXAucHkKcHl0aG9uMyBnZXQtcGlwLnB5IC0tdXNlcgpwaXAzIGluc3RhbGwgYXdzZWJjbGkgLS11cGdyYWRlIC0tdXNlcgpwaXAzIGluc3RhbGwgLVUgcG9seWdvbi1hcGktY2xpZW50CnBpcDMgaW5zdGFsbCBzY2hlZHVsZQpwaXAzIGluc3RhbGwgbWFpbGpldC1yZXN0CnBpcDMgaW5zdGFsbCBib3RvMwplY2hvICdleHBvcnQgZW49RUMyJyA+PiB+Ly5iYXNocmMKZWNobyAnZXhwb3J0IHRlc3Q9YmJmZGVhNTlhYTFjNzMyYjM3ZjY2ZDVjN2ZkM2ZlMDgnID4+IH4vLmJhc2hyYwplY2hvICdleHBvcnQgdG16PXBzdCcgPj4gfi8uYmFzaHJjCmVjaG8gJ2V4cG9ydCBUcmVuZD11cCcgPj4gfi8uYmFzaHJjCnNvdXJjZSB+Ly5iYXNoX3Byb2ZpbGUKc291cmNlIH4vLmJhc2hyYwpta2RpciB+L0RhdGFTdG9yZQp0b3VjaCB+L0RhdGFTdG9yZS90cmVuZC50eHQKbWtkaXIgfi93b3Jrc3BhY2UKc3VkbyBkbmYgaW5zdGFsbCBnaXQtYWxsIC15CmNkIH4vd29ya3NwYWNlCmdpdCBjbG9uZSBodHRwczovL2dpdGh1Yi5jb20vYWJ1cm1kL3JlYWxUaW1lUXVvdGVzLmdpdApjZCB+Cm5vaHVwIHB5dGhvbjMgfi93b3Jrc3BhY2UvcmVhbFRpbWVRdW90ZXMvdGVzdC5weSAm"

# Create an EC2 resource
ec2 = boto3.resource('ec2')

# Create a new EC2 instance
def create():
    instances = ec2.create_instances(
        ImageId='ami-0a3c3a20c09d6f377',  # Replace with the AMI ID of your choice
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',  # Modify as needed
        KeyName='abu_personal',  # Replace with your key pair name
        UserData=user_data_script 
    )
    return instances[0].id

res=create()

print("New instance created:", res)