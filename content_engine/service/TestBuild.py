#!/usr/local/bin/python2.7

import sys
sys.path.append("..")

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

import socket, struct

from portal.models import Game
from BuildIndex import Index

if __name__ == '__main__':
    index = Index("../testdb")

    index.CreateDB()
    for game in Game.objects.filter(id = 98):
        print game.id
        tags = []
        for t in game.tags.all():
            tags.append(t.name)
        cats = [game.category.name, ]
        index.BuildIndexForOne(index.db, index.logger, game.pk, game.name, game.description, cats, tags)




