# YaDraw

YaDraw is a super-simple graphical interface built on top of pygame.
The key use case is when you have a program which performs some calculations, 
and you want to add super-simple visualization to it. YaDraw supports basic primitives and shapes.

### Minimal example
```python
import yadraw.yadraw as yd
import time

# Create a window
window = yd.Window()

# Draw a circle
window.circle(center=(100, 100), radius=10, color=(0, 0, 255))
window.update()

# Close after 5 seconds
time.sleep(5)
window.close()
```


### Async draw example
Suppose you have a calculation which you want to visualize in real time:
- You have an ongoing calculation (a for loop in this case). 
- The result of this calculation (in this case list_of_points_to_draw) is dynamically updated and needs visualization during calculation.
- The pace of producing results and the pace of visualization (e.i. fps) should be independent.


```python
import yadraw.yadraw as yd
import time


# Create a custom on_redraw handler
def custom_on_redraw(self: yd.Window):
    self.fill((200, 200, 200))  # Fill entire screen with grey color 
    for point in list_of_points_to_draw:  # For each already calculated point
        self.circle(center=point, radius=4, color=(0, 0, 255))  # Draw a blue circle at this point

        
# Monkey-patch the on_redraw handler for yd.Window class
yd.Window.on_redraw = custom_on_redraw

# Create a window, set automatic update to 1 second interval = 1 fps.
window = yd.Window(auto_update_s=1)

# Start the "calculation" of the points to draw
list_of_points_to_draw = []
for i in range(100):
    list_of_points_to_draw.append((i * 8, i * 8))
    time.sleep(0.1)  # around 10 dots per frame

# Await GUI exit (i.e. wait for the user to close the window) 
window.wait_until_exit()
```
>[Github](https://github.com/EmixD/yadraw)

