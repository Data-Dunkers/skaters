migrate((db) => {
    const dao = new Dao(db);

    const createCollection = (name, schemaFields) => {
        try {
            dao.findCollectionByNameOrId(name);
        } catch (_) {
            const publicApiRule = "";
            const collection = new Collection({
                name: name,
                type: "base",
                listRule: publicApiRule,
                viewRule: publicApiRule,
                createRule: publicApiRule,
                updateRule: "",
                deleteRule: ""
            });

            schemaFields.forEach(f => collection.schema.addField(f));

            dao.saveCollection(collection);
        }
    };

    // 1. Photos Collection
    createCollection("data_skaters_photos", [
        new SchemaField({ name: "event_key", type: "text" }),
        new SchemaField({ name: "nickname",  type: "text" }),
        new SchemaField({ name: "real_name", type: "text" }),
        new SchemaField({ 
            name: "photo",     
            type: "file", 
            options: { maxSelect: 1, maxSize: 5242880, mimeTypes: ["image/jpeg", "image/png", "image/webp"] } 
        })
    ]);

    // 2. Shots Collection
    createCollection("data_skaters_shots", [
        new SchemaField({ name: "event_key",  type: "text" }),
        new SchemaField({ name: "nickname",   type: "text" }),
        new SchemaField({ name: "group",      type: "number" }),
        new SchemaField({ name: "distance",   type: "number" }),
        new SchemaField({ name: "shots_made", type: "number" })
    ]);

    // 3. Traits Collection
    createCollection("data_skaters_traits", [
        new SchemaField({ name: "event_key",          type: "text" }),
        new SchemaField({ name: "nickname",           type: "text" }),
        new SchemaField({ name: "height_cm",          type: "number" }),
        new SchemaField({ name: "wingspan_cm",        type: "number" }),
        new SchemaField({ name: "skate_size",         type: "number" }),
        new SchemaField({ name: "handedness",         type: "text" }),
        new SchemaField({ name: "birth_month",        type: "text" }),
        new SchemaField({ name: "reaction_time_ms",   type: "number" }),
        new SchemaField({ name: "resting_heart_rate", type: "number" })
    ]);

    // 4. Rocket League Collection
    createCollection("data_skaters_rocket_league", [
        new SchemaField({ name: "event_key",  type: "text" }),
        new SchemaField({ name: "nickname",   type: "text" }),
        new SchemaField({ name: "score",      type: "number" }),
        new SchemaField({ name: "goals",      type: "number" }),
        new SchemaField({ name: "assists",    type: "number" }),
        new SchemaField({ name: "saves",      type: "number" }),
        new SchemaField({ name: "shots",      type: "number" })
    ]);
});