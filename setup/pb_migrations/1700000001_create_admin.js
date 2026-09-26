migrate((db) => {
    const dao = new Dao(db);

    const email = $os.getenv("PB_ADMIN_EMAIL") || "service@datadunkers.ca";
    const password = $os.getenv("PB_ADMIN_PASSWORD") || "datadunkers";

    try {
        dao.findAdminByEmail(email);
    } catch (_) {
        const admin = new Admin();
        admin.email = email;
        admin.setPassword(password);
        dao.saveAdmin(admin);
    }
}, (db) => {
    const dao = new Dao(db);
    const email = $os.getenv("PB_ADMIN_EMAIL") || "service@datadunkers.ca";
    try {
        dao.deleteAdmin(dao.findAdminByEmail(email));
    } catch (_) {}
});
