import sys
import mysql.connector as mysql

class Tree:

    db = mysql.connect(
        host = "192.168.62.11",
        user = "root",
        passwd = "xE2j!b5pi2S-D641WW8fnLWNZBmdR-N2",
        database = "octavia"
        )

    _flag = False

    def set_flag(self,flag):
        if flag.lower() == "delete":
                Tree._flag = True


    def __init__(self,label,children=[]):
            self.label = label
            self.children = children

    def print_tree(self,parent_id,parent_name="load_balancer"):
        if not self.children:
            print(self.label.upper())
            if Tree._flag:
                  self.delete_info(parent_id,parent_name)
            else:
                  print(self.show_info(parent_id,parent_name))


        else:

            for node_id in self.get_root_id(parent_id,parent_name):
                node_id=node_id[0]
                #print(node_id,type(node_id))

                for child in self.children:
                    child.print_tree(node_id,self.label)

                print(self.label.upper())

            if Tree._flag:
                  self.delete_info(parent_id,parent_name)
            else:
                  print(self.show_info(parent_id,parent_name))

    def get_root_id(self,parent_id,parent_name):
        #print(parent_name)
        cursor = Tree.db.cursor()
        if self.label == "load_balancer":
                cursor.execute("select id from {} where name='{}'".format(self.label,parent_id))
        else:
        	cursor.execute("select id from {} where {}_id='{}'".format(self.label,parent_name,parent_id))
        return cursor.fetchall()

    def show_info(self,parent_id,parent_name):
        #import pdb;pdb.set_trace()
        #print(parent_name)
        cursor = Tree.db.cursor()
        if self.label == "load_balancer":
                cursor.execute("select id from {} where name='{}'".format(self.label,parent_id))
        else:
        	cursor.execute("select * from {} where {}_id='{}'".format(self.label,parent_name,parent_id))
        return cursor.fetchall()

    def delete_info(self,parent_id,parent_name):
        cursor = Tree.db.cursor()
        if self.label == "load_balancer":
                cursor.execute("delete from {} where name='{}'".format(self.label,parent_id))
                Tree.db.commit()
        else:
                cursor.execute("delete from {} where {}_id='{}'".format(self.label,parent_name,parent_id))
 #       return cursor.fetchall()


if __name__ == "__main__":

    n = Tree("load_balancer",[Tree("amphora"),Tree("vip"),Tree("vrrp_group"),Tree("listener",[Tree("sni"),Tree("l7policy",[Tree("l7rule")])]),Tree("pool",[Tree("member"),Tree("session_persistence"),Tree("health_monitor")])])
    n.set_flag(sys.argv[1])
    n.print_tree(sys.argv[2])
