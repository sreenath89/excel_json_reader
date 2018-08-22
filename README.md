## Excel to Json Converter


**Workflow:**

1. Download the xlsx file from - https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.xls
2. Store the xlsx
3. Go through the file and find the sheet titled "MICs List by CC"
4. Create a list of dicts. The contents in the first row must be used as the keys for the dict.
5. Write the above contents into a json file.

**Steps for Creating Lambda package**

1. Create the Project directory
2. Save all of your Python source files (the .py files) at the root level of this directory.
3. Install any libraries using pip. Again, you install these libraries at the root level of the directory.

```
pip install module-name -t /path/to/project-dir
```

For example, the following command installs the requests HTTP library in the project-dir directory.
```
pip install requests -t /path/to/project-dir
```

5. Zip the content of the project-dir directory, which is your deployment package.


**IMP**

1. Proper permissions must be given for doing S3 operations.
This can be done from IAM console (https://console.aws.amazon.com/iam/)
2. Zip the directory content contained within the directory, not the directory itself.
3. Bucket name used is steeleyetest
