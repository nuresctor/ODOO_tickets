from odoo import fields, models, api
from odoo.exceptions import Warning
class Book(models.Model):
    _sql_constraints = [
        ('library_book_name_date_uq',  # Constraint unique identifier
         'UNIQUE (name, date_published)',  # Constraint SQL syntax
         'Book title and publication date must be unique.'),  # Message
        ('library_book_check_date',
         'CHECK (date_published <= current_date)',
         'Publication date must not be in the future.'),
    ]
    _name = 'library.book'
    _description = 'Book'
    _order = 'name, date_published desc'

    name = fields.Char(
        'Title',
        default=None,
        index=True,
        help='Book cover title.',
        readonly=False,
        required=True,
        translate=False,
    )
    isbn = fields.Char('ISBN')

    book_type = fields.Selection(
        [('paper', 'Paperback'),
         ('hard', 'Hardcover'),
         ('electronic', 'Electronic'),
         ('other', 'Other')],
        'Type')
    notes = fields.Text('Internal Notes')
    descr = fields.Html('Description')
    # Numeric fields:
    copies = fields.Integer(default=1)
    avg_rating = fields.Float('Average Rating', (3, 2))
    price = fields.Monetary('Price', 'currency_id')
    currency_id = fields.Many2one('res.currency')  # price helper
    # Date and time fields:
    date_published = fields.Date()
    last_borrow_date = fields.Datetime(
        'Last Borrowed On',
        default=lambda self: fields.Datetime.now())

    active = fields.Boolean('Active?', default=True)
    image = fields.Binary('Cover')
    publisher_id = fields.Many2one('res.partner', string='Publisher')

    #author_ids = fields.Many2many('res.partner', string='Authors')
    # Book <-> Authors relation (using positional args)
    author_ids = fields.Many2many(
        'res.partner',  # related model (required)
        'library_book_res_partner_rel',  # relation table name to use
        'a_id',  # rel table field for "this" record
        'p_id',  # rel table field for "other" record
        'Authors')  # string label text

    #computed field

    publisher_country_id = fields.Many2one(
        'res.country', string='Publisher Country (related)',
        #related='publisher_id.country_id',
        compute='_compute_publisher_country',
        # store = False,  # Default is not to store in db
        inverse='_inverse_publisher_country',
        search='_search_publisher_country',
    )

    def _search_publisher_country(self, operator, value):
        return [('publisher_id.country_id', operator, value)]

    def _inverse_publisher_country(self):
        for book in self:
            book.publisher_id.country_id = book.publisher_country_id

    @api.depends('publisher_id.country_id')
    def _compute_publisher_country(self):
        for book in self:
            book.publisher_country_id = book.publisher_id.country_id

    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise Warning('Please provide an ISBN for %s' % book.name)
            if book.isbn and not book._check_isbn():
                raise Warning('%s is an invalid ISBN' % book.isbn)
        return True

