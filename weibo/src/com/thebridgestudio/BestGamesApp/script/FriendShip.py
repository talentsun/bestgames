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
    def CheckCommonFollow(cls, client, uid1, uid2, count_=10):
        ret = client.get.friendships__friends__in_common(uid=uid1, suid=uid2, count=count_)
        return ret.total_number
        
