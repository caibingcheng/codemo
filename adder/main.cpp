#include <iostream>

using namespace std;

template <typename T>
class calc
{
public:
    calc() : m_result(0) {}
    calc(const T &t) : m_result(t) {}
    auto add(const T &t) -> decltype(this)
    {
        m_result += t;
        return this;
    }

    auto sub(const T &t) -> decltype(this)
    {
        m_result -= t;
        return this;
    }

    auto set() -> decltype(this)
    {
        T tmp;
        cin >> tmp;
        m_result += tmp;
        return this;
    }

    friend ostream &operator<<(ostream &out, const calc *c)
    {
        out << c->m_result;
        return out;
    }

private:
    T m_result = static_cast<T>(0);
};

int main()
{
    calc<int> sum[1] = {1};

    cout << sum
                ->set()
                ->add(1)
                ->add(2)
                ->add(3)
                ->add(4)
                ->sub(2)
                ->add(4)
                ->sub(2)
         << endl;
}