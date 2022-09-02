from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class ProductQuantityWizard(models.TransientModel):
    _name = 'produced.qty.wizard'

    qty = fields.Float('Produced Quantity')

    def action_create(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        workorder = self.env['mrp.workorder'].browse([rec_model.id])

        pre_order = self.env['mrp.workorder'].search(
            [('id', '=', workorder.id - 1), ('production_id', '=', workorder.production_id.id)])
        qty_producing = 0
        if pre_order:
            for pre in pre_order.production_id.produced_lines:
                if pre.name == pre_order.name and pre.workcenter_id.id == pre_order.workcenter_id.id:
                    qty_producing = qty_producing + pre.qty
        else:
            qty_producing = workorder.production_id.qty_producing

        # if self.qty > qty_producing:
        #     raise ValidationError('Produced Quantity can not be greater than Quantity to Produce')

        qty = 0
        for line in workorder.production_id.produced_lines:
            if line.name == workorder.name and line.workcenter_id.id == workorder.workcenter_id.id:
                qty = qty + line.qty
        # if self.qty > (qty_producing - qty):
        #     raise ValidationError('You are trying to produce more quantity than initial demand.')

        rec = self.env['produced.qty.line'].create({
            'mrp_id': workorder.production_id.id,
            'name': rec_model.name,
            'workcenter_id': rec_model.workcenter_id.id,
            'qty': self.qty,
            'paused_date': datetime.today(),
            'start_date': rec_model.start_date_custom,
        })


class QuantityDoneWizard(models.TransientModel):
    _name = 'done.qty.wizard'

    qty = fields.Float('Produced Quantity')
    reasons = fields.Char()
    # reason = fields.Selection([
    #     ('wrong', 'Wrong Cutting'),
    #     ('burn', 'Burn'),
    #     ('hole', 'Hole'),
    #     ('shortage', 'Shortage of material during welding'),
    #     ('excess', 'Excess of material during welding'),
    # ], string='Reason', default='', ondelete='cascade')

    def action_create(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        workorder = self.env['mrp.workorder'].browse([rec_model.id])
        pre_order = self.env['mrp.workorder'].search(
            [('id', '=', workorder.id - 1), ('production_id', '=', workorder.production_id.id)])
        qty_producing = 0
        if pre_order:
            for pre in pre_order.production_id.produced_lines:
                if pre.name == pre_order.name and pre.workcenter_id.id == pre_order.workcenter_id.id:
                    print(pre.qty)
                    qty_producing = qty_producing + pre.qty
        else:
            qty_producing = workorder.production_id.qty_producing

        # if self.qty > qty_producing:
        #     raise ValidationError('Produced Quantity can not be greater than Quantity to Produce')

        qty = 0
        for line in workorder.production_id.produced_lines:
            if line.name == workorder.name and line.workcenter_id.id == workorder.workcenter_id.id:
                qty = qty + line.qty
        # if self.qty > (qty_producing - qty):
        #     raise ValidationError('You are trying to produce more quantity than initial demand.')
        if self.qty + qty < qty_producing:
            if not self.reasons:
                raise UserError('Please add reason of rejection.')
            reject = self.env['reason.line'].create({
                'mrp_id': workorder.production_id.id,
                'name': workorder.name,
                'workcenter_id': workorder.workcenter_id.id,
                'qty': qty_producing - (self.qty + qty),
                'reasons': self.reasons,
                'paused_date': datetime.today(),
                'start_date': workorder.start_date_custom,
            })
        if self.qty > 0:
            res = self.env['produced.qty.line'].create({
                'mrp_id': workorder.production_id.id,
                'name': workorder.name,
                'workcenter_id': workorder.workcenter_id.id,
                'qty': self.qty,
                'paused_date': datetime.today(),
                'start_date': workorder.start_date_custom,
            })
        work_list = []
        for w_line in workorder.production_id.workorder_ids:
            work_list.append(w_line.id)
        p_qty = 0
        if work_list:
            if work_list[-1] == workorder.id:
                for p_line in workorder.production_id.produced_lines:
                    if p_line.name == workorder.name and p_line.workcenter_id.id == workorder.workcenter_id.id:
                        p_qty = p_qty + p_line.qty
                workorder.production_id.qty_producing = p_qty
        record = self.button_finish(workorder)

    def button_finish(self, order):
        end_date = datetime.now()
        for workorder in order:
            if workorder.state in ('done', 'cancel'):
                continue
            workorder.end_all()
            vals = {
                'state': 'done',
                'date_finished': end_date,
                'date_planned_finished': end_date
            }
            if not workorder.date_start:
                vals['date_start'] = end_date
            if not workorder.date_planned_start or end_date < workorder.date_planned_start:
                vals['date_planned_start'] = end_date
            workorder.write(vals)

            workorder._start_nextworkorder()
        return True
