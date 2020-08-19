class Role:
    alluser_perm=["update_post","delete_post","create_post","delete_account","view_orders","add_order"] # every user can delete, change and update yourself post
    special_perm=["view_orders_of_others"]

    def __init__(self,user):
        self.user=user
        self.perm=self.data()
    
    def data(self):
        data=list(self.user.get_user_permissions())
        print(data)
        return data


    