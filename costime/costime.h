#include <sys/time.h>
#include <tuple>
#include <type_traits>

template <typename Func, typename... Args>
static typename std::enable_if<std::is_void<typename std::result_of<Func(Args...)>::type>::value,
                               double>::type
costTimeMs(Func &&func, Args &&... args)
{
    auto get_time_us = []() -> double {
        struct timeval time;
        gettimeofday(&time, NULL);
        double ms = time.tv_sec * 1000.0 + time.tv_usec / 1000.0;
        return ms;
    };

    double start = get_time_us();
    func(args...);
    double end = get_time_us();

    double cost = end - start;

    return cost;
}

template <typename Func, typename... Args>
static
    typename std::enable_if<!(std::is_void<typename std::result_of<Func(Args...)>::type>::value),
                            std::tuple<double, typename std::result_of<Func(Args...)>::type>>::type
    costTimeMs(Func &&func, Args &&... args)
{
    using RT = typename std::result_of<Func(Args...)>::type;
    std::tuple<double, RT> ret;
    auto nfunc = [&]() -> void { std::get<1>(ret) = func(args...); };
    std::get<0>(ret) = costTimeMs(nfunc);

    return ret;
}
