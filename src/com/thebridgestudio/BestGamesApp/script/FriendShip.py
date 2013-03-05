#!/usr/bin/python


class FriendShip:
    @classmethod
    def Follow(cls, client, uid_):
        client.post.friendships__create(uid=uid_)


    @classmethod
    def Unfollow(cls, client, uid_):
        client.post.friendships__destroy(uid=uid_)


    @classmethod
    def CheckFollow(cls, client, uidFrom, uidTo):
        ret = client.get.friendships__show(source_id=uidFrom, target_id=uidTo)

        return ret.source.following 

    @classmethod
    def CheckCommonFollow(cls, client, checkUid):
        
