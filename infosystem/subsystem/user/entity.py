# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity
from infosystem.database import db


class User(entity.Entity, db.Model):

    attributes = ['id', 'domain_id', 'name', 'email', 'active']
    domain_id = db.Column(db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
    __table_args__ = (UniqueConstraint('domain_id', 'name', name='user_name_uk'),UniqueConstraint('domain_id', 'email', name='user_email_uk'),)

    def __init__(self, id, domain_id, name, email, password, active=True):
        super(User, self).__init__(id)
        self.domain_id = domain_id
        self.name = name
        self.email = email
        self.password = password
        self.active = active
