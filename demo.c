int factorial(int x)
{
    if (x)
    {
        int nextX;

        nextX = x - 1;

        return x * factorial(nextX);
    }
    else
        return 1;
}

int linear(int w, int b, int x)
{
    int result;

    result = b + w * x;

    return result;
}

int main(int x)
{
    int w;
    int result;

    x = 7;
    w = 10;

    {
        int b;

        b = 16;

        result = factorial(linear(w / 3, -b, x));
    }

    return result;
}
