/**
 * IndexedDB Database Manager for CodeClash
 * Handles all client-side database operations
 */

const DB_NAME = 'CodeClashDB';
const DB_VERSION = 2;
let db = null;

/**
 * Initialize IndexedDB
 */
async function initDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);

        request.onerror = () => {
            console.error('Database failed to open:', request.error);
            reject(request.error);
        };

        request.onsuccess = () => {
            db = request.result;
            console.log('✅ Database initialized successfully');
            resolve(db);
        };

        request.onupgradeneeded = (event) => {
            db = event.target.result;
            console.log('🔄 Upgrading database...');

            // Create challenges object store
            if (!db.objectStoreNames.contains('challenges')) {
                const challengeStore = db.createObjectStore('challenges', { keyPath: 'id', autoIncrement: true });
                challengeStore.createIndex('title', 'title', { unique: false });
                challengeStore.createIndex('difficulty', 'difficulty', { unique: false });
                console.log('✅ Created challenges store');
            }

            // Create matches object store
            if (!db.objectStoreNames.contains('matches')) {
                const matchStore = db.createObjectStore('matches', { keyPath: 'id', autoIncrement: true });
                matchStore.createIndex('challenge_id', 'challenge_id', { unique: false });
                matchStore.createIndex('status', 'status', { unique: false });
                matchStore.createIndex('created_at', 'created_at', { unique: false });
                console.log('✅ Created matches store');
            }

            // Create solved challenges object store
            if (!db.objectStoreNames.contains('solved_challenges')) {
                const solvedStore = db.createObjectStore('solved_challenges', { keyPath: 'problem_number' });
                solvedStore.createIndex('difficulty', 'difficulty', { unique: false });
                solvedStore.createIndex('programming_language', 'programming_language', { unique: false });
                solvedStore.createIndex('solved_at', 'solved_at', { unique: false });
                solvedStore.createIndex('time_elapsed', 'time_elapsed', { unique: false });
                console.log('✅ Created solved_challenges store');
            }

            console.log('✅ Database upgrade complete');
        };
    });
}

/**
 * Challenge CRUD Operations
 */
const ChallengeDB = {
    /**
     * Add a new challenge
     */
    async add(challenge) {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['challenges'], 'readwrite');
            const store = transaction.objectStore('challenges');
            
            const request = store.add({
                ...challenge,
                created_at: challenge.created_at || new Date().toISOString()
            });

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get all challenges
     */
    async getAll() {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['challenges'], 'readonly');
            const store = transaction.objectStore('challenges');
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get challenge by ID
     */
    async getById(id) {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['challenges'], 'readonly');
            const store = transaction.objectStore('challenges');
            const request = store.get(id);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get challenges by difficulty
     */
    async getByDifficulty(difficulty) {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['challenges'], 'readonly');
            const store = transaction.objectStore('challenges');
            const index = store.index('difficulty');
            const request = index.getAll(difficulty);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Update a challenge
     */
    async update(id, updates) {
        return new Promise(async (resolve, reject) => {
            try {
                const challenge = await this.getById(id);
                if (!challenge) {
                    reject(new Error('Challenge not found'));
                    return;
                }

                const transaction = db.transaction(['challenges'], 'readwrite');
                const store = transaction.objectStore('challenges');
                const request = store.put({ ...challenge, ...updates });

                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            } catch (error) {
                reject(error);
            }
        });
    },

    /**
     * Delete a challenge
     */
    async delete(id) {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['challenges'], 'readwrite');
            const store = transaction.objectStore('challenges');
            const request = store.delete(id);

            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Clear all challenges
     */
    async clear() {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['challenges'], 'readwrite');
            const store = transaction.objectStore('challenges');
            const request = store.clear();

            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }
};

/**
 * Match CRUD Operations
 */
const MatchDB = {
    /**
     * Add a new match
     */
    async add(match) {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['matches'], 'readwrite');
            const store = transaction.objectStore('matches');
            
            const request = store.add({
                challenge_id: match.challenge_id,
                status: match.status || 'active',
                player_code: match.player_code || null,
                player_errors: match.player_errors || 0,
                player_time: match.player_time || 0,
                player_submitted: match.player_submitted || false,
                player_completed: match.player_completed || false,
                started_at: match.started_at || new Date().toISOString(),
                ended_at: match.ended_at || null,
                created_at: new Date().toISOString()
            });

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get all matches
     */
    async getAll() {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['matches'], 'readonly');
            const store = transaction.objectStore('matches');
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get match by ID
     */
    async getById(id) {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['matches'], 'readonly');
            const store = transaction.objectStore('matches');
            const request = store.get(id);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get matches by challenge ID
     */
    async getByChallengeId(challengeId) {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['matches'], 'readonly');
            const store = transaction.objectStore('matches');
            const index = store.index('challenge_id');
            const request = index.getAll(challengeId);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Update a match
     */
    async update(id, updates) {
        return new Promise(async (resolve, reject) => {
            try {
                const match = await this.getById(id);
                if (!match) {
                    reject(new Error('Match not found'));
                    return;
                }

                const transaction = db.transaction(['matches'], 'readwrite');
                const store = transaction.objectStore('matches');
                const request = store.put({ ...match, ...updates });

                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            } catch (error) {
                reject(error);
            }
        });
    },

    /**
     * Delete a match
     */
    async delete(id) {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['matches'], 'readwrite');
            const store = transaction.objectStore('matches');
            const request = store.delete(id);

            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Clear all matches
     */
    async clear() {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['matches'], 'readwrite');
            const store = transaction.objectStore('matches');
            const request = store.clear();

            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }
};

/**
 * Solved Challenges CRUD Operations
 */
const SolvedChallengesDB = {
    /**
     * Save a solved challenge
     */
    async save(challenge) {
        if (!db) {
            await initDB();
        }
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['solved_challenges'], 'readwrite');
            const store = transaction.objectStore('solved_challenges');
            
            const request = store.put({
                problem_number: challenge.problem_number,
                problem_name: challenge.problem_name,
                difficulty: challenge.difficulty,
                programming_language: challenge.programming_language,
                time_elapsed: challenge.time_elapsed,
                solved_at: challenge.solved_at || new Date().toISOString()
            });

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get all solved challenges
     */
    async getAll() {
        if (!db) {
            await initDB();
        }
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['solved_challenges'], 'readonly');
            const store = transaction.objectStore('solved_challenges');
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get solved challenge by problem number
     */
    async getById(problemNumber) {
        if (!db) {
            await initDB();
        }
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['solved_challenges'], 'readonly');
            const store = transaction.objectStore('solved_challenges');
            const request = store.get(problemNumber);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get solved challenges by difficulty
     */
    async getByDifficulty(difficulty) {
        if (!db) {
            await initDB();
        }
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['solved_challenges'], 'readonly');
            const store = transaction.objectStore('solved_challenges');
            const index = store.index('difficulty');
            const request = index.getAll(difficulty);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get solved challenges by language
     */
    async getByLanguage(language) {
        if (!db) {
            await initDB();
        }
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['solved_challenges'], 'readonly');
            const store = transaction.objectStore('solved_challenges');
            const index = store.index('programming_language');
            const request = index.getAll(language);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Get statistics
     */
    async getStats() {
        const all = await this.getAll();
        
        const stats = {
            total: all.length,
            byDifficulty: {
                foundational: 0,
                easy: 0,
                average: 0,
                difficult: 0
            },
            byLanguage: {},
            averageTime: 0,
            fastestTime: null,
            slowestTime: null,
            recentlySolved: []
        };

        if (all.length === 0) return stats;

        let totalTime = 0;
        let fastest = Infinity;
        let slowest = 0;

        all.forEach(challenge => {
            // Count by difficulty
            if (stats.byDifficulty.hasOwnProperty(challenge.difficulty)) {
                stats.byDifficulty[challenge.difficulty]++;
            }

            // Count by language
            if (!stats.byLanguage[challenge.programming_language]) {
                stats.byLanguage[challenge.programming_language] = 0;
            }
            stats.byLanguage[challenge.programming_language]++;

            // Calculate time stats
            totalTime += challenge.time_elapsed;
            if (challenge.time_elapsed < fastest) {
                fastest = challenge.time_elapsed;
                stats.fastestTime = challenge;
            }
            if (challenge.time_elapsed > slowest) {
                slowest = challenge.time_elapsed;
                stats.slowestTime = challenge;
            }
        });

        stats.averageTime = Math.floor(totalTime / all.length);

        // Get 5 most recently solved
        stats.recentlySolved = all
            .sort((a, b) => new Date(b.solved_at) - new Date(a.solved_at))
            .slice(0, 5);

        return stats;
    },

    /**
     * Delete a solved challenge
     */
    async delete(problemNumber) {
        if (!db) {
            await initDB();
        }
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['solved_challenges'], 'readwrite');
            const store = transaction.objectStore('solved_challenges');
            const request = store.delete(problemNumber);

            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    },

    /**
     * Clear all solved challenges
     */
    async clear() {
        if (!db) {
            await initDB();
        }
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['solved_challenges'], 'readwrite');
            const store = transaction.objectStore('solved_challenges');
            const request = store.clear();

            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }
};

/**
 * Initialize database and load initial data if needed
 */
async function initializeDatabase() {
    try {
        await initDB();
        
        // Check if we need to seed initial data
        const challenges = await ChallengeDB.getAll();
        if (challenges.length === 0) {
            console.log('📊 Database empty, loading challenges...');
            await loadChallengesFromServer();
        }
    } catch (error) {
        console.error('❌ Database initialization failed:', error);
    }
}

/**
 * Load challenges from server (via API endpoint)
 */
async function loadChallengesFromServer() {
    try {
        const response = await fetch('/api/challenges/data');
        if (response.ok) {
            const challenges = await response.json();
            
            // Clear existing challenges
            await ChallengeDB.clear();
            
            // Add each challenge
            for (const challenge of challenges) {
                await ChallengeDB.add(challenge);
            }
            
            console.log(`✅ Loaded ${challenges.length} challenges from server`);
        }
    } catch (error) {
        console.error('❌ Failed to load challenges from server:', error);
    }
}

// Initialize database when script loads
if (typeof window !== 'undefined') {
    window.addEventListener('DOMContentLoaded', initializeDatabase);
    // Make SolvedChallengesDB globally available
    window.SolvedChallengesDB = SolvedChallengesDB;
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { initDB, ChallengeDB, MatchDB, SolvedChallengesDB, initializeDatabase };
}
