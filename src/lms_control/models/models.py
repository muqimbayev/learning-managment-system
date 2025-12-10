from odoo import models, fields

class ScheduleTable(models.Model):
    _inherit = "le.schedule_student_lesson"

    attendance = fields.Boolean(string="Attended", default=False)


class ScheduleLesson(models.Model):
    _inherit = "le.schedule.lesson"

    def button_passed(self):
        # 1. Joriy darsga (self) bog'langan o'quvchilarning ID'larini olamiz.
        # Bu erda self.group_id.student_ids.ids kerak bo'lishi mumkin, ammo
        # eng muhimi, allaqachon yaratilgan *dars-o'quvchi* yozuvlarini filtrlaymiz.
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendance',
            'res_model': 'le.schedule_student_lesson',
            'view_mode': 'list', # 'list' o'rniga Odoo'da ko'pincha 'tree' ishlatiladi.
            
            # Action ichida faqat List View'ni ochish uchun 'views' kaliti to'g'ri.
            'views': [(self.env.ref('lms_control.attendance_lesson_view').id)], 
            
            'target': 'new',
            
            # 2. ENG MUHIM QISM: Joriy darsga tegishli yozuvlarni filtrlash.
            # Agar le.schedule_student_lesson modelida 'lesson_id' maydoni mavjud bo'lsa:
            'domain': [('lesson_id', '=', self.id)],
            
            # 3. CONTEXT: Agar davomat yozuvi yaratilmagan bo'lsa, yangi yozuvlarni yaratish uchun 
            # 'lesson_id' ning default qiymatini berishimiz mumkin.
            'context': {
                'default_lesson_id': self.id,
                # Agar siz faqat 'active' talabalarni istasangiz:
                # 'default_student_id_domain': [('status', '=', 'active')]
            }
        }