/** @odoo-module **/

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";

const DashboardKanbanView = registry.category("views").get("account_dashboard_kanban")

class CustomDashboardKanbanController extends kanbanView.Controller {
     get progressBarAggregateFields() {
         const res = super.progressBarAggregateFields;
         const progressAttributes = this.props.archInfo.progressAttributes;
         if (progressAttributes && progressAttributes.recurring_revenue_sum_field) {
             res.push(progressAttributes.recurring_revenue_sum_field);
         }
         return res;
     }
 }
DashboardKanbanView.Controller = CustomDashboardKanbanController;