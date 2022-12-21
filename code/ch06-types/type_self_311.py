from typing import Optional, Self


class User:

    def __init__(self, next_id: int):
        self.id = next_id

    def same(self, other_user: Self) -> bool:
        return self.id == other_user.id


def user_by_id(user_id: int) -> Optional[User]:
    return User(user_id)


u1 = User(1)
u2 = User(2)

# u1.same(7)

print(f'Are u1 and u2 the same? {u1.same(u2)}')
