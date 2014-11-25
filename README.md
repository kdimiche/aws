# get\_sts\_token.py
##AWS CLI Credentials for MFA Accounts ##

With MFA enabled accounts, you need to generate session tokens (via STS) to use the AWS CLI tools.

### Requirements ###

- Python 2.7.8
- AWS CLI
- CLI configured with '~/.aws/config' containing header for each environment 

> [profile init_$ENVIRONMENT]  
> aws\_access\_key\_id = $AWS\_ACCESS\_KEY\_ID  
> aws\_secret\_access\_key = $AWS\_SECRET\_ACCESS\_KEY  

### Results ###

The script will use the credentials for init\_$ENVIRONMENT and create a new profile named "profile $ENVIRONMENT".

> [profile $ENVIRONMENT]  
> aws\_access\_key\_id = $AWS\_ACCESS\_KEY\_ID  
> aws\_secret\_access\_key = $AWS\_SECRET\_ACCESS\_KEY  

### Usage ###
#### Generate Session Credentials ####
`$ python get\_sts\_token.py -u kevin.dimichel --mfa\_token 761247 -e prd`

`$ python get\_sts\_token.py -u kevin.dimichel-dev --mfa\_token 761247 -e dev` 


#### Example of AWS CLI usage #### 
`$ aws iam list-roles --profile dev`

## Links ##
- http://boto.readthedocs.org/en/latest/ref/sts.html