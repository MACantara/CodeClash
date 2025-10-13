# CodeClash Matchmaking System Documentation

## Overview
The matchmaking system allows players to find opponents quickly and efficiently through various matching methods. The system is designed to minimize wait times while ensuring fair matches.

## Architecture

### Database Schema

#### Lobbies Table
- `id`: Unique identifier
- `name`: Room name (displayed to users)
- `host_id`: User who created the lobby
- `challenge_id`: The programming challenge for this lobby
- `difficulty_filter`: Optional difficulty preference
- `max_players`: Maximum capacity (default: 2)
- `current_players`: Current number of players
- `status`: waiting, in_match, or closed
- `is_public`: Visibility (1 = public, 0 = private)
- `created_at`: Timestamp of creation

#### Lobby Players Table
- `id`: Unique identifier
- `lobby_id`: Reference to lobbies table
- `user_id`: Reference to users table
- `joined_at`: Timestamp when player joined

#### Matches Table (Updated)
- Added `lobby_id`: Links match to originating lobby

## Matchmaking Methods

### 1. Quick Match
**Endpoint**: `POST /lobby/quick-match`

**How it works:**
1. Searches for available public lobbies with open slots
2. Excludes lobbies created by the requesting user
3. Optionally filters by difficulty level
4. If found: Joins existing lobby
5. If not found: Creates new lobby with random challenge
6. Auto-starts match when lobby reaches capacity

**Parameters:**
- `difficulty` (optional): "Easy", "Medium", or "Hard"

**Response:**
```json
{
  "success": true,
  "lobby_id": 123,
  "match_started": false,
  "created": true
}
```

### 2. Custom Room Creation
**Endpoint**: `POST /lobby/create`

**How it works:**
1. Validates user doesn't have existing active lobby
2. Creates new lobby with specified parameters
3. Adds creator as first player
4. Makes room visible in lobby browser (if public)

**Parameters:**
- `name`: Room name
- `challenge_id`: Specific challenge to play
- `is_public`: Visibility setting

**Use cases:**
- Playing specific challenges
- Waiting for friends
- Practicing particular problem types

### 3. Join Existing Room
**Endpoint**: `POST /lobby/{lobby_id}/join`

**How it works:**
1. Validates lobby exists and is available
2. Checks room isn't full
3. Checks player isn't already in lobby
4. Adds player to lobby_players table
5. Increments current_players count
6. Auto-starts match if room is now full

**Validation:**
- Lobby must be in "waiting" status
- Must have available slots
- Player can't be in multiple lobbies

## Real-time Updates

### Lobby List Polling
- **Frequency**: Every 5 seconds
- **Endpoint**: `GET /lobby/list`
- **Updates**: New lobbies, player counts, removed lobbies

### Player Status Polling
- **Frequency**: Every 2 seconds (when in lobby)
- **Endpoint**: `GET /lobby/{lobby_id}/status`
- **Updates**: 
  - Current player count
  - Lobby status changes
  - Match creation detection
  - Auto-redirect to match when ready

## User Experience Flow

### Quick Match Flow
```
User clicks "Quick Match"
    ↓
System searches for available lobbies
    ↓
[Found] → Join lobby → Wait for 2nd player → Auto-start match
    ↓
[Not Found] → Create lobby → Wait for opponent → Auto-start match
```

### Custom Room Flow
```
User clicks "Create Room"
    ↓
Fills in room details (name, challenge)
    ↓
Room created and visible in lobby browser
    ↓
Host waits in lobby (sees player status)
    ↓
Another player joins
    ↓
Match auto-starts
```

### Join Room Flow
```
User sees available rooms in lobby browser
    ↓
Clicks "Join" on desired room
    ↓
Added to lobby
    ↓
If room was waiting for 1 more player → Match starts immediately
    ↓
If room has slots available → Wait for more players
```

## Lobby Management

### Leaving Lobbies
**Endpoint**: `POST /lobby/{lobby_id}/leave`

**Rules:**
- Host leaving closes the entire lobby
- Non-host leaving decrements player count
- Empty lobbies are automatically closed
- Players are automatically removed when match starts

### Lobby Closure
Lobbies close when:
1. Host leaves
2. All players leave
3. Match successfully starts (status → "in_match")
4. Manual closure (future feature)

## Match Starting Logic

When a lobby reaches max capacity:
1. Retrieve all players in lobby (ordered by join time)
2. Create match with player1 and player2
3. Link match to lobby via `lobby_id`
4. Update lobby status to "in_match"
5. Return match_id to both players
6. Players auto-redirect to match page

## Security Considerations

### Implemented
- Session-based authentication required
- User can't match against themselves
- User can only be in one lobby at a time
- Lobby ownership validation

### Future Enhancements
- Rate limiting on lobby creation
- Anti-spam measures
- Report system for toxic behavior
- Private lobby passwords

## Performance Optimizations

### Current Implementation
- Polling-based updates (simple, reliable)
- Indexed database queries
- Efficient player count updates

### Future Improvements
- WebSocket integration for true real-time updates
- Redis for lobby caching
- Matchmaking queue system
- ELO-based matching

## Error Handling

### Common Errors
1. **"You already have an active lobby"**
   - User trying to create multiple lobbies
   - Solution: Leave current lobby first

2. **"Lobby is full"**
   - Attempting to join capacity-reached lobby
   - Solution: Race condition, find another lobby

3. **"Lobby not found"**
   - Lobby was closed/deleted
   - Solution: Refresh lobby list

4. **"Lobby is no longer available"**
   - Status changed from "waiting"
   - Solution: Match already started

## Testing Scenarios

### Test Case 1: Quick Match
1. User A clicks Quick Match
2. Verify lobby created
3. User B clicks Quick Match
4. Verify User B joins User A's lobby
5. Verify match auto-starts

### Test Case 2: Custom Room
1. User A creates custom room
2. Verify room appears in lobby list
3. User B joins room
4. Verify match starts immediately

### Test Case 3: Concurrent Matching
1. Multiple users click Quick Match simultaneously
2. Verify proper pairing
3. Verify no orphaned lobbies

### Test Case 4: Leave Lobby
1. User joins lobby
2. User leaves before match starts
3. Verify player removed
4. Verify lobby still available

## API Reference

### List Lobbies
```
GET /lobby/list
Returns: Array of lobby objects with host, challenge, and player info
```

### Create Lobby
```
POST /lobby/create
Body: { name, challenge_id, is_public }
Returns: { success, lobby_id }
```

### Join Lobby
```
POST /lobby/{lobby_id}/join
Returns: { success, lobby_id, match_started, match_id? }
```

### Leave Lobby
```
POST /lobby/{lobby_id}/leave
Returns: { success }
```

### Lobby Status
```
GET /lobby/{lobby_id}/status
Returns: { success, lobby, players, match_id? }
```

### Quick Match
```
POST /lobby/quick-match
Body: { difficulty? }
Returns: { success, lobby_id, match_started, created?, match_id? }
```

## Configuration

### Adjustable Parameters
- `max_players`: Change from 2 to support multiplayer
- Poll intervals: Adjust for performance vs. real-time needs
- Auto-close timers: Timeout for inactive lobbies
- Difficulty filters: Add more granular options

## Future Features

1. **ELO Matchmaking**: Match players of similar skill levels
2. **Ranked Mode**: Separate casual and competitive queues
3. **Tournament Mode**: Bracket-style multi-round competitions
4. **Team Battles**: 2v2 or team-based coding challenges
5. **Spectator Mode**: Watch matches in progress
6. **Lobby Chat**: Communication before match starts
7. **Private Lobbies**: Password-protected rooms
8. **Custom Match Settings**: Time limits, specific constraints
9. **Rematch System**: Quick rematches after games
10. **Friend Invites**: Direct invitation system

## Conclusion

The matchmaking system provides a robust, scalable foundation for connecting players. The polling-based approach ensures reliability while the modular design allows for easy enhancement with WebSockets or more advanced matchmaking algorithms in the future.
