# Wall Visibility Algorithm - Solution

## Problem Statement

Given a 2D floor plan made of wall rectangles, determine which walls are visible from each orthographic direction (top/bottom/left/right) - i.e., which walls should be colored blue in the "back view", "front view", etc.

---

## TL;DR for Interview

> "I used **backface culling**. Each wall rectangle contributes two vertices to a polygon outline. I walk around the walls, picking shared midpoints to form a CCW polygon. For each edge, the outward normal is 90° CCW from the edge direction. A wall is visible if `dot(normal, view_vector) < 0`."

---

## Hidden Surface Removal Algorithms

| Algorithm               | Use Case                                            | Why Not Here                            |
| ----------------------- | --------------------------------------------------- | --------------------------------------- |
| **Backface culling**    | Our solution - check if surface normal faces viewer | Simple, O(n), perfect for orthographic  |
| **Painter's algorithm** | Overlapping polygons, draw back-to-front            | No overlap in our 2D outline            |
| **Z-buffer**            | Per-pixel depth testing for complex 3D scenes       | Overkill for 2D, no depth variation     |
| **Ray casting**         | Arbitrary viewpoints, partial occlusion             | We have orthographic axis-aligned views |

**If asked about extensions**: For arbitrary camera angles or partial wall occlusion, ray casting would be the next step.

---

## The Algorithm: Polygon-Based Backface Culling

### Step 1: Convert Walls to Polygon

Each wall is a thick rectangle with 4 points. The **short edges** are the "ends" of the wall.

```
Wall rectangle:
  ┌─────────────────┐
  │                 │  ← long edge (side)
  └─────────────────┘
  ↑                 ↑
  short edge        short edge
  (midpoint A)      (midpoint B)
```

**Key insight**: Adjacent walls share a vertex! Wall 0's midpoint B ≈ Wall 1's midpoint A.

So for n walls → n unique vertices → closed polygon.

### Step 2: Build the Polygon

```python
for each wall i:
    vertex[i] = shared midpoint between wall[i-1] and wall[i]
```

Edge i (from vertex[i] to vertex[i+1]) corresponds to **wall i**.

### Step 3: Compute Normals

For a CCW polygon, the outward normal is 90° CCW from the edge direction:

```python
edge_direction = vertex[i+1] - vertex[i]
normal = (-edge_direction.y, edge_direction.x)  # 90° CCW rotation
normal = normalize(normal)
```

### Step 4: Visibility Test

```python
view_vectors = {
    TOP:    (0, -1),   # Looking down (Y decreases)
    BOTTOM: (0,  1),   # Looking up (Y increases)
    LEFT:   (1,  0),   # Looking right (X increases)
    RIGHT:  (-1, 0),   # Looking left (X decreases)
}

visible = dot(normal, view_vector) < 0
```

If dot product < 0 → normal points opposite to view → wall faces viewer → **visible**.

**Note**: View vector points FROM viewer TOWARD scene.

---

## Why This Works

1. **Walls form a continuous boundary** - they connect in order
2. **CCW winding is consistent** - verified by positive signed area
3. **90° CCW rotation always gives outward normal** for CCW polygons
4. **Dot product sign** tells us if vectors point same or opposite direction

---

## Results on Test Data

```
TOP (back):     walls [6, 8, 10, 12]   ← The 4 horizontal "staircase" edges
BOTTOM (front): walls [0, 2, 4, 14, 16, 17]
LEFT:           walls [11, 13, 18]
RIGHT:          walls [1, 3, 5, 7, 9, 15]
```

---

## Implementation Files

```
generators/visibility.py     # Core algorithm
  - Vector2D, Segment        # Data types
  - get_short_edge_midpoints()
  - build_polygon_vertices() # Walls → polygon
  - get_visible_wall_indices() # Main API

tests/test_visibility.py     # Unit tests
```

---

## Interview Talking Points

### Why backface culling?

- O(n) complexity - just one dot product per wall
- Perfect for orthographic axis-aligned views
- No need for complex occlusion handling

### Why not convex hull?

- Building is **non-convex** (has staircase shape)
- Convex hull would lose the interior recesses
- We need ALL boundary walls, not just the outer envelope

### The tricky part?

- Wall rectangles don't directly give us the polygon
- Had to extract midpoints and handle the **shared vertices**
- Winding order matters - CCW gives correct outward normals

### How to extend?

- **Arbitrary camera angles**: Still backface culling, just different view vectors
- **Partial occlusion**: Would need ray casting or scanline algorithm
- **3D buildings**: Z-buffer or proper 3D rendering pipeline

### Complexity?

- **Time**: O(n) per view direction, O(4n) = O(n) for all 4 directions
- **Space**: O(n) for the polygon vertices

---

## Core Logic (Pseudocode)

```python
def get_visible_wall_indices(walls, direction):
    # Step 1: Build polygon from wall midpoints
    vertices = []
    for i in range(n):
        shared = find_shared_midpoint(walls[i-1], walls[i])
        vertices.append(shared)

    # Step 2: Check each edge
    view = get_view_vector(direction)
    visible = set()

    for i in range(n):
        edge = vertices[(i+1) % n] - vertices[i]
        normal = Vector2D(-edge.y, edge.x).normalize()

        if dot(normal, view) < -EPSILON:
            visible.add(i)

    return visible
```

---

## Lessons Learned

1. **Think geometrically first** - walls → polygon → normals → dot product
2. **Winding order matters** - CCW vs CW determines normal direction
3. **Shared vertices simplify everything** - no need for complex centerline orientation
4. **Epsilon for floating point** - perpendicular walls have dot ≈ 0
