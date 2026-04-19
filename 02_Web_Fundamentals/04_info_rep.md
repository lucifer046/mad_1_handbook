# Information Representation

How do computers store text, images, and numbers using only bits (0 and 1)? This is the problem of **Encoding**.

## Binary & Numbers
At the lowest level, everything is binary. 
-   **Bits**: 0 or 1.
-   **Integers**: Represented in base-2. For example, $6_{10} = 110_2$.
-   **Negative Numbers**: Represented using **Two's Complement**. To find $-x$, you invert the bits of $x$ and add 1.

[NOTE]
**Example: -6 in 4-bit Two's Complement**
1. Start with $6$: `0110`
2. Invert bits: `1001`
3. Add 1: `1010` (This is -6)
[/CALLOUT]

## Text Encoding

### ASCII (1963)
The American Standard Code for Information Interchange was a 7-bit code that could represent 128 characters. It was sufficient for English but failed for international languages.

### Unicode
Unicode is a universal standard that assigns a unique number (**Code Point**) to every character in every language.
-   **UCS-2**: 16-bit (fixed length).
-   **UCS-4**: 32-bit (fixed length).

### UTF-8: The Web Standard
UTF-8 is a variable-length encoding that is backwards compatible with ASCII. It uses 1 to 4 bytes per character.

| Bytes | Prefix Bits | Free Bits | Range of Code Points |
| :--- | :--- | :--- | :--- |
| 1 | `0` | 7 | U+0000 to U+007F (ASCII) |
| 2 | `110` | 11 | U+0080 to U+07FF |
| 3 | `1110` | 16 | U+0800 to U+FFFF |
| 4 | `11110` | 21 | U+10000 to U+10FFFF |

[TIP]
UTF-8 is efficient because it uses only 1 byte for the most common characters (English/ASCII) while still supporting all characters in the world.
[/CALLOUT]

## Markup vs Style
-   **Markup**: Specifies the structure and meaning (e.g., HTML tags).
-   **Style**: Specifies the visual presentation (e.g., CSS).

## Glossary
- **Bit**: Binary Digit — the smallest unit of data.
- **Encoding**: The process of converting data into a specific format for storage or transmission.
- **Endianness**: The order of bytes in a multi-byte data type (Big-endian vs Little-endian).
