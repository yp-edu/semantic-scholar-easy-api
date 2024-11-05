# ---------------------------------------------------------------------------------------------------------------------
# CREATE RESOURCE GROUP
# ---------------------------------------------------------------------------------------------------------------------

resource "azurerm_resource_group" "rg" {
  count    = var.rg == null ? 1 : 0
  name     = "${var.app_name}-rg"
  location = var.location

  tags = {
    managed_by = "terraform"
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE APP SERVICE PLAN
# ---------------------------------------------------------------------------------------------------------------------

resource "azurerm_service_plan" "as_plan" {
  count               = var.as_plan == null ? 1 : 0
  name                = "${var.app_name}-as"
  resource_group_name = var.rg == null ? azurerm_resource_group.rg.0.name : var.rg.name
  location            = var.rg == null ? azurerm_resource_group.rg.0.location : var.rg.location
  os_type             = "Linux"
  sku_name            = "B1"
  worker_count        = 1

  tags = {
    managed_by = "terraform"
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE AZURE CONTAINER REGISTRY
# ---------------------------------------------------------------------------------------------------------------------

resource "azurerm_container_registry" "acr" {
  count               = var.acr == null ? 1 : 0
  name                = "${var.app_name}acr"
  resource_group_name = var.rg == null ? azurerm_resource_group.rg.0.name : var.rg.name
  location            = var.rg == null ? azurerm_resource_group.rg.0.location : var.rg.location
  sku                 = "Basic"

  tags = {
    managed_by = "terraform"
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# BLOCKLOADS APP
# ---------------------------------------------------------------------------------------------------------------------

resource "azurerm_linux_web_app" "app" {
  name                = "${var.app_name}-app"
  resource_group_name = var.rg == null ? azurerm_resource_group.rg.0.name : var.rg.name
  location            = var.as_plan == null ? azurerm_service_plan.as_plan.0.location : var.as_plan.location
  service_plan_id     = var.as_plan == null ? azurerm_service_plan.as_plan.0.id : var.as_plan.id
  https_only          = true

  identity {
    type = "SystemAssigned"
  }

  lifecycle {
    ignore_changes = [site_config]
  }

  site_config {
    container_registry_use_managed_identity = true
  }

  tags = {
    managed_by = "terraform"
  }
}

resource "azurerm_role_assignment" "app" {
  role_definition_name = "AcrPull"
  scope                = var.acr == null ? azurerm_container_registry.acr.0.id : var.acr.id
  principal_id         = azurerm_linux_web_app.app.identity.0.principal_id
}
