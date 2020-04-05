import boto3
# https://support.vastdata.com/hc/en-us/articles/360035029714-Using-Boto-3-with-VAST-Cluster-S3

ACCESS_ID = '164e099a19377f8a13efddca766514a8f6d01b56f768a327ec103ecec8d87a8a'
ACCESS_KEY = 'xxxxxxx'
bucket = 'western-wheelers'

class S3:
    def set_perm(selfself, cl, obj_id):
        s3 = boto3.resource('s3')
        object_acl = s3.ObjectAcl(bucket, obj_id + ".png")
        response = object_acl.put(ACL='public-read')
        #print("PERM", response)

    def upload_file(self, obj_id, file_name):
        s3_client = boto3.client('s3')
        # try:
        #file_name = 'images/'+obj_id+".png"
        response = s3_client.upload_file(file_name, bucket, obj_id+".png")
        #print("UPLOAD", response)

        #result = s3_client.get_bucket_acl(Bucket=bucket)
        #print("ACL:", result)
        result = s3_client.list_objects(
            Bucket = bucket,
        )
        # for res in result["Contents"]:
        #     print ("OBJS", res)

        self.set_perm(s3_client, obj_id)
        print ("uploaded", obj_id)
        # except ClientError as e:
        #     logging.error(e)
        #     return False


# s3 = boto3.resource('s3')
# s3.meta.client.upload_file('images/pm1.png', 'mybucket', 'hello.txt')
#upload_file('pm3')