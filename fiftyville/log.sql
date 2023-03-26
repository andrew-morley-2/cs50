-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Check crime_scene_reports table
SELECT * FROM crime_scene_reports;

-- Check atm_transactions table
SELECT * FROM atm_transactions;

-- Check flights table
SELECT * FROM flights;

-- Check bakery_security_logs table
SELECT * FROM bakery_security_logs;

-- Check interviews table
SELECT * FROM interviews;

-- Check bank_accounts table
SELECT * FROM bank_accounts;

-- Check airports table
SELECT * FROM airports;

-- Check passengers table
SELECT * FROM passengers;

-- Check phone_calls table
SELECT * FROM phone_calls;

-- Check people table
SELECT * FROM people;

-- Check crime scene reports for July 28, 2021
SELECT * FROM crime_scene_reports WHERE year = '2021' AND month = '07' and day = '28';

-- Check crime scene reports for July 28, 2021 on Humphrey Street
SELECT * FROM crime_scene_reports WHERE year = '2021' AND month = '07' and day = '28' AND street = 'Humphrey Street';

-- Get all incident information from crime_scene_reports for themft of CS50 duck
SELECT * FROM crime_scene_reports WHERE year = '2021' AND month = '07' and day = '28' AND street = 'Humphrey Street' AND description LIKE '%duck%';

-- Get id from crime_scene_reports for themft of CS50 duck
SELECT id FROM crime_scene_reports WHERE year = '2021' AND month = '07' and day = '28' AND street = 'Humphrey Street' AND description LIKE '%duck%';

-- Get all interviews for 7/28/21 that mention the bakery
SELECT * FROM interviews WHERE year = '2021' AND month = '07' and day = '28' AND transcript LIKE '%bakery%';

-- Result from interview query mentions security footage, ATM withdrawal, earliest flight out of Fiftyville on 7/29, and a phone call.

-- Get security logs from the bakery for time frame within 10 minutes of the theft
SELECT * FROM bakery_security_logs WHERE year = '2021' AND month = '07' and day = '28' AND hour = '10' AND minute >= '05' AND minute <= '25';

-- Get license plate from security logs from the bakery for time frame within 10 minutes of the theft
SELECT license_plate FROM bakery_security_logs WHERE year = '2021' AND month = '07' and day = '28' AND hour = '10' AND minute >= '05' AND minute <= '25';

-- Get phone call logs for day of theft that lasted for less than a minute
SELECT * FROM phone_calls WHERE year = '2021' AND month = '07' and day = '28' AND duration <= '60';

-- Get distinct callers from phone call logs for day of theft that lasted for less than a minute
SELECT DISTINCT(caller) FROM phone_calls WHERE year = '2021' AND month = '07' and day = '28' AND duration <= '60';

-- Get atm transactions logs for day of theft for withdrawal at ATM location on Leggett Street
SELECT * FROM atm_transactions WHERE year = '2021' AND month = '07' and day = '28' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Get distinct account numbers from atm transactions logs for day of theft for withdrawal at ATM location on Leggett Street
SELECT DISTINCT(account_number) FROM atm_transactions WHERE year = '2021' AND month = '07' and day = '28' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Get person ids from bank accounts based on account numbers associated with the theft
SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT DISTINCT(account_number) FROM atm_transactions WHERE year = '2021' AND month = '07' and day = '28' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw');

-- Get people records based on suspicious phone numbers, ATM transactions, bank account numbers, and license plates
SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT DISTINCT(account_number) FROM atm_transactions WHERE year = '2021' AND month = '07' AND day = '28' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw')) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = '2021' AND month = '07' and day = '28' AND hour = '10' AND minute >= '05' AND minute <= '25') AND phone_number IN (SELECT DISTINCT(caller) FROM phone_calls WHERE year = '2021' AND month = '07' and day = '28' AND duration <= '60');

-- Get passport number in people records based on suspicious phone numbers, ATM transactions, bank account numbers, and license plates
SELECT passport_number FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT DISTINCT(account_number) FROM atm_transactions WHERE year = '2021' AND month = '07' and day = '28' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw')) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = '2021' AND month = '07' and day = '28' AND hour = '10' AND minute >= '05' AND minute <= '25') AND phone_number IN (SELECT DISTINCT(caller) FROM phone_calls WHERE year = '2021' AND month = '07' and day = '28' AND duration <= '60');

-- Find Fiftyville airport id
SELECT id from airports WHERE city = 'Fiftyville';

-- Find id for earliest flight out of Fiftyville on 7/29 from flights
SELECT id FROM flights WHERE year = '2021' AND month = '07' and day = '29' AND origin_airport_id IN (SELECT id from airports WHERE city = 'Fiftyville') ORDER BY hour LIMIT 1;

-- Find passenger on earliest flight of of Fiftyville on 7/29 based on two suspects and their information from earlier queries
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE year = '2021' AND month = '07' and day = '29' AND origin_airport_id IN (SELECT id from airports WHERE city = 'Fiftyville') ORDER BY hour LIMIT 1) AND passport_number IN (SELECT passport_number FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT DISTINCT(account_number) FROM atm_transactions WHERE year = '2021' AND month = '07' and day = '28' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw')) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = '2021' AND month = '07' and day = '28' AND hour = '10' AND minute >= '05' AND minute <= '25') AND phone_number IN (SELECT DISTINCT(caller) FROM phone_calls WHERE year = '2021' AND month = '07' and day = '28' AND duration <= '60')));

-- Find destination city for earliest flight out of Fiftyville on 7/29 from flights
SELECT full_name from airports WHERE id IN (SELECT destination_airport_id FROM flights WHERE year = '2021' AND month = '07' and day = '29' AND origin_airport_id IN (SELECT id from airports WHERE city = 'Fiftyville') ORDER BY hour LIMIT 1);

-- Find phone number of accomplice
SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE duration <= '60' AND year = '2021' AND month = '07' AND day = '28' AND caller IN (SELECT phone_number FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE year = '2021' AND month = '07' and day = '29' AND origin_airport_id IN (SELECT id from airports WHERE city = 'Fiftyville') ORDER BY hour LIMIT 1) AND passport_number IN (SELECT passport_number FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT DISTINCT(account_number) FROM atm_transactions WHERE year = '2021' AND month = '07' and day = '28' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw')) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = '2021' AND month = '07' and day = '28' AND hour = '10' AND minute >= '05' AND minute <= '25') AND phone_number IN (SELECT DISTINCT(caller) FROM phone_calls WHERE year = '2021' AND month = '07' and day = '28' AND duration <= '60')))));