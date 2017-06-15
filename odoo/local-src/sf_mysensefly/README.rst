This module provides an interface between the ERP and Sensefly website.
The interface class implements a generic method "call" to be called through xmlrpc.

# Example:
    ``sock.execute(db, uid, password, 'sf.mysensefly.interface', 'call', 'get_spare_parts', [1, 1])``

The method to be called (in the example get_spare_parts) might be implemented or not.
