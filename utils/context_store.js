// context-store.js
class ContextStore {
    constructor() {
        this.dbName = 'projectContexts';
        this.storeName = 'contexts';
        this.db = null;
        this.init();
    }

    async init() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, 1);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve();
            };
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                const store = db.createObjectStore(this.storeName, { keyPath: 'id' });
                store.createIndex('projectId', 'projectId', { unique: false });
                store.createIndex('updated', 'updated', { unique: false });
            };
        });
    }

    async saveContext(context) {
        const tx = this.db.transaction(this.storeName, 'readwrite');
        const store = tx.objectStore(this.storeName);
        
        const contextObj = {
            id: crypto.randomUUID(),
            projectId: context.projectId,
            title: context.title,
            content: context.content,
            created: new Date(),
            updated: new Date()
        };
        
        await store.put(contextObj);
    }

    async getContext(id) {
        const tx = this.db.transaction(this.storeName, 'readonly');
        const store = tx.objectStore(this.storeName);
        return await store.get(id);
    }

    async exportToFile(contextId) {
        const context = await this.getContext(contextId);
        const blob = new Blob([context.content], { type: 'text/markdown' });
        
        try {
            const handle = await window.showSaveFilePicker({
                suggestedName: `${context.title}.md`,
                types: [{
                    description: 'Markdown',
                    accept: { 'text/markdown': ['.md'] },
                }],
            });
            
            const writable = await handle.createWritable();
            await writable.write(blob);
            await writable.close();
        } catch (err) {
            console.error('Failed to save file:', err);
        }
    }
}