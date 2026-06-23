# Design Document — Fill This Out BEFORE Writing Any Code

The whole point of this exercise is to externalize your thinking before coding.
Treat blank sections as failure conditions — if you cannot fill a section,
you are not ready to start coding that part yet.

---

## Section 0: What does the existing code do?

In your own words, describe the existing system in 4–6 bullet points.
What classes exist? What does each own? What is the matching strategy?

*(If you cannot do this from memory after reading once, read again. Do not skip.)*

-

---

## Section 1: Reuse vs Replace

For each existing class, decide and justify:

| Class       | Reuse / Modify / Replace | Why |
|-------------|--------------------------|-----|
| `Driver`    |                          |     |
| `Rider`     |                          |     |
| `Ride`      |                          |     |
| `Dispatcher`|                          |     |

This is the most important section. Most interview failures happen because this
decision was made implicitly, mid-coding, instead of explicitly upfront.

---

## Section 2: New Nouns

What new classes / enums / types are you introducing?

| New thing | Kind (class / enum / value) | Data it owns | Why it must exist |
|-----------|-----------------------------|--------------|-------------------|
|           |                             |              |                   |
|           |                             |              |                   |
|           |                             |              |                   |

---

## Section 3: Ownership Decisions

Answer all of these before coding.

1. Where does `Location` live as a type? Who imports it?

2. Who owns the matching strategy (nearest driver)? Is it a method on
   `Dispatcher`, or a separate class? Why?

3. Where does fare calculation live? On `Dispatcher`, on `Ride`, or somewhere else?

4. Does `Ride` know about its `Driver`? Does `Driver` know about its current `Ride`? Both? Neither?

5. Where do the state-transition rules live (e.g. "you can't start a CANCELLED ride")?
   On the enum, on the `Ride`, on the `Dispatcher`, or elsewhere?

---

## Section 4: Walk-Through

Trace through this scenario in plain English (no code):

> Alice (at 0,0) and Bob (at 10,10) both go online.
> Carol requests a ride from (1,0) to (4,4).
> The ride is started.
> A surge of 2.0x is set.
> Dave requests a ride from (10,10) to (15,10).
> Carol's ride is cancelled.

At each step:
- Which driver is in which state?
- Which ride is in which state?
- What is each ride's fare? Why?

---

## Section 5: Edge Cases

Before opening a `.py` file, list at least 4 edge cases your code must handle.

1.
2.
3.
4.

---

## Section 6: Post-Coding Reflection *(fill in after you finish)*

- Did your code match the design? Where did it diverge, and why?
- If you went back to fix something mid-coding, what was it, and would the design
  doc have caught it if you had thought harder upfront?

*(Two or three sentences. This is the most important section for building the habit.)*
