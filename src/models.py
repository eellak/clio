from app import db
from sqlalchemy.ext.associationproxy import association_proxy

# Middle table that connects component and license
component_license_conn = db.Table("component_license_conn",
                                  db.Column("component_id", db.Integer,
                                            db.ForeignKey("component.id")),
                                  db.Column("license_id", db.Integer,
                                            db.ForeignKey("license.id"))
                                  )

# Middle table that connects two components
component_conn = db.Table("component_conn",
                          db.Column("parent_id", db.Integer,
                                    db.ForeignKey("component.id")),
                          db.Column("child_id", db.Integer,
                                    db.ForeignKey("component.id"))
                          )


# Middle table that connects product and component
class Product_Component_conn(db.Model):
    __tablename__ = "product_component_conn"

    product_id = db.Column(db.Integer, db.ForeignKey("product.id"),
                           primary_key=True)

    component_id = db.Column(db.Integer, db.ForeignKey("component.id"),
                             primary_key=True)

    # Relationship
    relation = db.Column(db.String(128))

    # Modification
    modification = db.Column(db.Boolean)

    # Delivery
    delivery = db.Column(db.String(128))

    product = db.relationship("Product", back_populates="component_conn")

    component = db.relationship("Component", back_populates="product_conn")

    def __init__(self, product=None, component=None, relation=None,
                 modification=None, delivery=None):
        self.product = product
        self.component = component
        self.relation = relation
        self.modification = modification
        self.delivery = delivery


class Component(db.Model):
    """Represents a Component.
    A component can be associated with more than one License.
    A component can either be simple or complex.
    """
    __tablename__ = "component"

    # Component ID
    id = db.Column(db.Integer, primary_key=True)

    # Component Name
    name = db.Column(db.String(128), unique=True, nullable=False)

    # Component Version
    version = db.Column(db.String(128), nullable=False)

    # Created on
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           nullable=False)

    # Created by
    created_by = db.Column(db.String(128))

    # Publication Date
    pub_date = db.Column(db.DateTime)

    # Origin website
    origin = db.Column(db.String(128))

    # Source URL
    source_url = db.Column(db.String(128))

    # Content
    content = db.Column(db.String(128))

    # External Links
    ext_link = db.Column(db.String(128))

    # Licenses
    licenses = db.relationship("License", secondary="component_license_conn",
                               backref=db.backref("component", lazy="dynamic"),
                               lazy="dynamic"
                               )

    # Components
    components = db.relationship("Component", secondary="component_conn",
                                 primaryjoin=id == component_conn.c.parent_id,
                                 secondaryjoin=id == component_conn.c.child_id,
                                 backref=db.backref("component",
                                                    lazy="dynamic"),
                                 lazy="dynamic"
                                 )

    product_conn = db.relationship(
        "Product_Component_conn", back_populates="component")

    def __init__(self, name, version, pub_date=None, origin=None, source_url=None, ext_link=None):

        self.name = name
        self.version = version
        self.pub_date = pub_date
        self.origin = origin
        self.source_url = source_url
        self.ext_link = ext_link


class License(db.Model):
    """Represents a License."""
    __tablename__ = "license"

    # License ID
    id = db.Column(db.Integer, primary_key=True)

    # Fullname
    full_name = db.Column(db.String(128), nullable=False)

    # Identifier
    identifier = db.Column(db.String(128), unique=True, nullable=False)

    # FSF Free/Libre
    fsf_free_libre = db.Column(db.Boolean)

    # OSI Approved
    osi_approved = db.Column(db.Boolean)

    # License Category
    license_category = db.Column(db.String(128))

    # License Text
    license_text = db.Column(db.Text)

    product = db.relationship('Product', cascade='all, delete-orphan',
                              backref='license', lazy='dynamic')

    def __init__(self, full_name, identifier, fsf_free_libre=None,
                 osi_approved=None, license_category=None, license_text=None):

        self.full_name = full_name
        self.identifier = identifier
        self.fsf_free_libre = fsf_free_libre
        self.osi_approved = osi_approved
        self.license_category = license_category
        self.license_text = license_text


class Product(db.Model):
    """Represents a Product"""
    __tablename__ = "product"

    # Product ID
    id = db.Column(db.Integer, primary_key=True)

    # Name
    name = db.Column(db.String(128), unique=True, nullable=False)

    # Version
    version = db.Column(db.String(128), nullable=False)

    # Out-Bound License (OBL)
    license_id = db.Column(db.Integer, db.ForeignKey('license.id'))

    # Owner
    owner = db.Column(db.String(128))

    # Approver
    approver = db.Column(db.String(128))

    # Approval Date
    approval_date = db.Column(db.DateTime)

    component_conn = db.relationship(
        "Product_Component_conn", back_populates="product")

    def __init__(self, name, version, owner=None, approver=None, approval_date=None):
        self.name = name
        self.version = version
        self.owner = owner
        self.approver = approver
        self.approval_date = approval_date
