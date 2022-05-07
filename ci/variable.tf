variable "region" {
  default = "us-east-1"
}

variable "key_spec" {
  default = "SYMMETRIC_DEFAULT"
}

variable "enabled" {
  default = true
}

variable "kms_alias" {
  default = "my_kms_key"
}

variable "rotation_enabled" {
  default = true
}
