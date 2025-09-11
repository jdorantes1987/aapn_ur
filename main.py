from process_permission import ProcessPermission
from role_manager import User
from user_role import UserRole

if __name__ == "__main__":
    # 1. Crear roles
    admin_role = UserRole("Administrador")
    billing_role = UserRole("Facturación")
    viewer_role = UserRole("Visualizador")

    # 2. Definir permisos para los procesos
    # El rol de Administrador tiene todos los permisos en Facturación
    admin_billing_permissions = ProcessPermission(
        read=True, create=True, update=True, delete=True
    )
    admin_role.add_permission("facturacion", admin_billing_permissions)

    # El rol de Facturación puede leer, crear y actualizar, pero no eliminar
    billing_permissions = ProcessPermission(
        read=True, create=True, update=True, delete=False
    )
    billing_role.add_permission("facturacion", billing_permissions)

    # El rol de Visualizador solo puede leer
    viewer_permissions = ProcessPermission(read=True)
    viewer_role.add_permission("facturacion", viewer_permissions)

    # 3. Crear usuarios y asignarles roles
    user_admin = User("admin_user")
    user_admin.assign_role(admin_role)

    user_billing = User("billing_user")
    user_billing.assign_role(billing_role)

    user_viewer = User("viewer_user")
    user_viewer.assign_role(viewer_role)

    # 4. Verificar permisos

    print(
        f"--- Verificando permisos para {user_billing.username} con rol '{next(iter(user_billing.roles)).name}' ---"
    )
    print(
        f"¿Puede leer en Facturación? {'✅' if user_billing.has_permission('facturacion', 'read') else '❌'}"
    )
    print(
        f"¿Puede crear en Facturación? {'✅' if user_billing.has_permission('facturacion', 'create') else '❌'}"
    )
    print(
        f"¿Puede actualizar en Facturación? {'✅' if user_billing.has_permission('facturacion', 'update') else '❌'}"
    )
    print(
        f"¿Puede eliminar en Facturación? {'✅' if user_billing.has_permission('facturacion', 'delete') else '❌'}"
    )

    print("\n" + "=" * 50 + "\n")

    print(
        f"--- Verificando permisos para {user_viewer.username} con rol '{next(iter(user_viewer.roles)).name}' ---"
    )
    print(
        f"¿Puede leer en Facturación? {'✅' if user_viewer.has_permission('facturacion', 'read') else '❌'}"
    )
    print(
        f"¿Puede crear en Facturación? {'✅' if user_viewer.has_permission('facturacion', 'create') else '❌'}"
    )
