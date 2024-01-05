import folium

folium_map = folium.Map(location=[48.866667,  2.333333],
                        zoom_start=13,
                        tiles="CartoDB dark_matter")
marker = folium.CircleMarker(location=[48.866667,  2.333333])
marker.add_to(folium_map)

folium_map.save("my_map.html")