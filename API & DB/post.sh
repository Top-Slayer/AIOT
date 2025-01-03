while true
do
    curl -X POST http://localhost:5000/led -H "Content-Type: application/x-www-form-urlencoded" -d "color=red&action=on"
    sleep 1
    curl -X POST http://localhost:5000/led -H "Content-Type: application/x-www-form-urlencoded" -d "color=green&action=on"
    sleep 1
    curl -X POST http://localhost:5000/led -H "Content-Type: application/x-www-form-urlencoded" -d "color=blue&action=on"
    sleep 1
    curl -X POST http://localhost:5000/led -H "Content-Type: application/x-www-form-urlencoded" -d "color=blue&action=off"
    sleep 1
    curl -X POST http://localhost:5000/led -H "Content-Type: application/x-www-form-urlencoded" -d "color=green&action=off"
    sleep 1
    curl -X POST http://localhost:5000/led -H "Content-Type: application/x-www-form-urlencoded" -d "color=red&action=off"
    sleep 1

    curl -X POST http://localhost:5000/led -H "Content-Type: application/x-www-form-urlencoded" -d "color=blue&action=on"
    sleep 1
    curl -X POST http://localhost:5000/led -H "Content-Type: application/x-www-form-urlencoded" -d "color=green&action=on"
    sleep 1
    curl -X POST http://localhost:5000/led -H "Content-Type: application/x-www-form-urlencoded" -d "color=red&action=on"
    sleep 1
    curl -X POST http://localhost:5000/led -H "Content-Type: application/x-www-form-urlencoded" -d "color=red&action=off"
    sleep 1
    curl -X POST http://localhost:5000/led -H "Content-Type: application/x-www-form-urlencoded" -d "color=green&action=off"
    sleep 1
    curl -X POST http://localhost:5000/led -H "Content-Type: application/x-www-form-urlencoded" -d "color=blue&action=off"
    sleep 1
done