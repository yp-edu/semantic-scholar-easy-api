# ---------------------------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------------------------------------------------------------------------------

variable "rg" {
  type        = any
  default     = null
  description = "Resource group. If null, a new resource group will be created."
}

variable "as_plan" {
  type        = any
  default     = null
  description = "App Service Plan. If null, an F1 plan will be created."
}

variable "acr" {
  type        = any
  default     = null
  description = "Azure Container Registry. If null, a new ACR will be created."
}

# ---------------------------------------------------------------------------------------------------------------------
# INPUT VARIABLES
# ---------------------------------------------------------------------------------------------------------------------

variable "app_name" {
  type        = string
  description = "Name of the app."
}

variable "location" {
  type        = string
  default     = "westeurope"
  description = "Location of the resources."
}
